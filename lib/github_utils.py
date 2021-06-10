from github import Github, Repository
import os

TOKEN = 'GITHUB_TOKEN'
INDRA_REPO = 'INDRA_REPO'
token = os.getenv(TOKEN, None)

BASE_BRANCH = 'master'

HEAD_BRANCH = 'staging'

ORGANIZATION = 'TandonDevOps'

REPO_NAME = os.getenv(INDRA_REPO, 'IndraABM')

"""
Since I am using my own github account, the PR's are authored by me.
Due to this, I cannot add myself as a reviewer automatically.
Solution: Create a GitHub app/bot to create the PR.
"""
REVIEWERS = ['Denisfench', 'gcallah', 'NathanConroy']


def pr_already_exists(repo: Repository.Repository):
    pull_requests = repo.get_pulls(base=BASE_BRANCH, head=HEAD_BRANCH)
    if pull_requests.totalCount != 0:
        return True, pull_requests
    else:
        return False, None


def generate_pr():
    if not token:
        raise EnvironmentError(
            "Could not find github token. It is required to make an API "
            "call to create a PR. "
            "Please set it in your environment and re-start the build.")

    hub = Github(token)
    org = hub.get_organization(login=ORGANIZATION)
    repo = org.get_repo(name=REPO_NAME)
    # Do not try to create a new PR if there is a PR out already.
    pr_exists, pull_requests = pr_already_exists(repo)
    if not pr_exists:
        head_branch = repo.get_branch(HEAD_BRANCH)
        base_branch = repo.get_branch(BASE_BRANCH)
        head_commit = head_branch.commit
        body = head_commit.commit.message
        title = 'Auto PR due to push to staging'
        pr = repo.create_pull(base=base_branch.name, head=head_branch.name,
                              body=body,
                              maintainer_can_modify=True, title=title,)

        pr.create_review_request(reviewers=REVIEWERS, team_reviewers=[])
        print(f'Created PR: {pr.html_url}')
    else:
        print('PR already exists. The push should have updated the PR.')
        for pr in pull_requests:
            print(pr.html_url)


if __name__ == "__main__":
    generate_pr()
