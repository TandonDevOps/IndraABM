export user_type="test"
export test_dir="tests"
# just a dummy ignore we can change if we need to add somefin'
export ignores="FOO"
echo "$INDRA_HOME"

if [ -z "$1" ]; then
  export capture=""
else
  export capture="--nocapture"
fi

nosetests --ignore-files=$ignores --exe --verbose --with-coverage --cover-package=notebooks $capture
