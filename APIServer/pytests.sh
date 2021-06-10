export test_runner="nosetests"
# for some strange reason, some systems need to run python3 to get
# the right version of nosetests
if [ $USER = "nhipham" ] 
then 
	export test_runner="python3 /usr/local/bin/nosetests"
fi

export user_type="test"
export test_dir="tests"
export ignores="scheduler"  # dummy file!
export excludes="multithreaded_tests"

if [ -z "$1" ]
then
    export capture=""
else
    export capture="--nocapture"
fi

echo "INDRA_HOME: $INDRA_HOME"
$test_runner --ignore-files=$ignores --exclude=$excludes --exe --verbose --with-coverage --cover-package=APIServer $capture