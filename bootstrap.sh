#!/bin/bash
# :: bootstrap.sh
################################################
# Sets up the virtualenv, or
# destroys it, as needed.
################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 8 November 2018

##############################################
# CONSTANTS
##############################################
readonly PYTHON=python3
readonly PIP=pip3

##############################################
# ARGUMENT PARSING
##############################################
CLEAN=false

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -c|--clean)
    CLEAN=true
    shift # past argument
    shift # past value
    ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

##############################################
# FUNCTIONS
##############################################

# @param1: the name of the app/pkg to check for in the path
verifyPathInstallaton ()
{
  if $1 --version &> /dev/null; then
    return 0
  else
    return 1
  fi
}

buildVirtualEnv ()
{
  $PYTHON -m virtualenv build || return 1
  source build/bin/activate || return 1
  printf "Using virtualenv pip: "
  which pip
  pip install -r .bootstrap/requirements.txt || return 1
  deactivate || return 1
  return 0
}

##############################################
# MAIN
##############################################

main ()
{
  if $CLEAN; then
    echo "Cleaning..."
    rm -rf build
    rm -rf __pycache__
    find . -name "__pycache__" -exec rm -rf {} \;
    find . -name "*.pyc" -delete
    echo "Done!"
  else
    if [[ "$VIRTUAL_ENV" != "" ]]; then 
      echo "Already in a virtualenv. No need to bootstrap."
      exit 0
    fi
    if [ -f build/bin/python3 ] || [ -f build/bin/pip ] ; then
      echo "virtualenv already setup. No need to bootstrap. Did you mean to clean?"
      exit 0
    fi

    echo "Verifying dependencies..."
    if verifyPathInstallaton $PIP; then
      printf "\t✓ pip3 is available in the PATH\n"
    else
      printf "\t✗ pip3 is available in the PATH\n\n"
      echo "ERROR: could not find pip3 in the PATH. Please ensure you've installed pip3 and properly set your PATH variable."
      exit 1
    fi

    if verifyPathInstallaton $PYTHON; then
      printf "\t✓ python3 is available in the PATH\n"
    else
      printf "\t✗ python3 is available in the PATH\n\n"
      echo "ERROR: could not find python3 in the PATH. Please ensure you've installed python3 and properly set your PATH variable."
      exit 1
    fi

    if [[ $(pip list | grep -F virtualenv) != "" ]]; then
      printf "\t✓ virtualenv is installed\n\n"
    else
      printf "\t✗ virtualenv is installed\n"
      printf "ERROR: virtualenv not installed, acquiring...\n\n"
      python -m pip install --user virtualenv
      rc=$?; if [[ $rc != 0 ]]; then 
        printf "ERROR: virtualenv failed to install. Try cleaning (\`./bootstrap.sh -c\`) and re-bootstrapping.\n"
        exit $rc
      else
        printf "\n\t✓ virtualenv acquired successfully\n\n"
      fi
    fi


    echo "Building virtualenv..."
    echo "---"
    if buildVirtualEnv; then
      echo "---"
      echo "Successfully built virtualenv!"
      echo "Run \`source build/bin/activate\` from the root of the repo to engage the virtualenv."
    else
      echo "---"
      echo "ERROR: failed to build virtualenv. Try \`./bootstrap.sh --clean\`, and then re-run bootstrap."
      exit 1
    fi
  fi
  exit 0
}

main
