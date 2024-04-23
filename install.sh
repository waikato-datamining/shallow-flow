#!/bin/bash
#
# Script to install all the shallowflow repos in a virtual environment

# the usage of this script
function usage()
{
   echo
   echo "${0##*/} [-v <dir>] [-p <path>] [-y] [-l] [-h]"
   echo
   echo "Installs all the shallowflow repos in a virtual environment."
   echo
   echo " -h   this help"
   echo " -v   <dir>"
   echo "      the virtual environment directory to use, default: $VENV_DIR_DEFAULT"
   echo " -p   <path>"
   echo "      the path to the Python interpreter to use, default: $PYTHON_INTERPRETER_DEFAULT"
   echo " -y   whether to assume 'yes' for user prompts, "
   echo "      e.g., if the venv dir already exists and requires deleting"
   echo " -l   whether to install the latest, i.e., straight from the github repositories"
   echo "      rather than using the modules published on PyPI.org."
   echo
}

VENV_DIR_DEFAULT="./venv"
VENV_DIR=$VENV_DIR_DEFAULT
PYTHON_INTERPRETER_DEFAULT="/usr/bin/python3"
PYTHON_INTERPRETER=$PYTHON_INTERPRETER_DEFAULT
ASSUME_YES="no"
LATEST="no"

# interpret parameters
while getopts ":hylv:p:" flag
do
   case $flag in
      v) VENV_DIR=$OPTARG
         ;;
      p) PYTHON_INTERPRETER=$OPTARG
         ;;
      y) ASSUME_YES="yes"
         ;;
      l) LATEST="yes"
         ;;
      h) usage
         exit 0
         ;;
      *) usage
         exit 1
         ;;
   esac
done

echo
echo "shallowflow installation"
echo "========================"

# delete venv dir
if [ -d "$VENV_DIR" ]
then
  if [ ! "$ASSUME_YES" = "yes" ]
  then
    echo
    read -n 1 -p "Virtual environment '$VENV_DIR' exists - remove (y/n)? " ANSWER
    if [ "$ANSWER" != "y" ]
    then
      echo
      echo "Keeping the virtual environment, exiting script."
      echo
      exit 0
    else
      echo
    fi
  fi
  echo
  echo "Deleting virtual environment: $VENV_DIR"
  rm -R "$VENV_DIR"
fi

PIP="$VENV_DIR/bin/pip"

# create venv
echo
echo "Creating virtual environment: $VENV_DIR"
echo
$PYTHON_INTERPRETER -m venv "$VENV_DIR"

# update tools
"$VENV_DIR/bin/pip" install --upgrade pip wheel

# installing wai.annotation
echo
echo "Installing shallowflow modules..."
echo
if [ "$LATEST" = "yes" ]
then
  "$PIP" install \
      git+https://github.com/waikato-datamining/coed.git \
      git+https://github.com/waikato-datamining/shallowflow-api.git \
      git+https://github.com/waikato-datamining/shallowflow-base.git \
      git+https://github.com/waikato-datamining/shallowflow-cv2.git \
      git+https://github.com/waikato-datamining/shallowflow-redis.git \
      git+https://github.com/waikato-datamining/shallowflow-sklearn.git \
      git+https://github.com/waikato-datamining/shallowflow-vfs.git
else
  "$PIP" install shallowflow
fi

# done
SF_RUN="$VENV_DIR/bin/sf-runflow"
if [ -f "$SF_RUN" ]
then
  echo
  echo "Installation finished!"
  echo
  echo "You can now run flows directly as follows:"
  echo "  $SF_RUN [options]"
  echo
  echo "Or you can activate the virtual environment using this command:"
  echo "  . $VENV_DIR/bin/activate"
  echo
  echo "And then deactivate it again with this command:"
  echo "  deactivate"
  echo
else
  echo
  echo "Installation failed, check console output!"
  echo
fi
