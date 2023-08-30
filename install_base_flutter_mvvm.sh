#!/bin/bash

# Define the sed/gsed function
if [[ "$OSTYPE" == "darwin"* ]]; then
    SED=gsed
else
    SED=sed
fi

function create_folder {
    echo -e "\n*** Create mobile folder with base flutter project ***"

    # Create folder
    mkdir mobile

    # Create base flutter project
    flutter create --org $DOMAIN_NAME --project-name $PROJECT_NAME --template app --platforms android,ios ./mobile/

    echo "[DONE]"
}

function replace_lib {
    echo -e "\n*** Pull lib and assets from Git and replace them in project ***"

    # Pull git repository
    git clone git@bitbucket.org:deusesprl/base_flutter_mvvm.git ./base_flutter_mvvm

    # Remove lib folder
    rm -rf ./mobile/lib

    # Copy lib folder
    cp -r ./base_flutter_mvvm/lib ./mobile/

    # Add assets
    cp -r ./base_flutter_mvvm/assets ./mobile/

    echo "[DONE]"
}

function replace_pubspec_analysis_options {
    echo -e "\n*** Replace pubspec.yaml and analysis options of the created project ***"

    # Remove pubspec.yaml file
    rm ./mobile/pubspec.yaml

    # Remove analysis options file
    rm ./mobile/analysis_options.yaml

    # Copy pubspec.yaml file
    cp ./base_flutter_mvvm/pubspec.yaml ./mobile/

    # Copy analysis options file
    cp ./base_flutter_mvvm/analysis_options.yaml ./mobile/

    echo "[DONE]"
}

function replace_with_new_name {
    echo -e "\n*** Replace all the instances of PROJECT_NAME in the project with the new name ***"

    # Replace all the instances of PROJECT_NAME in the project with the new name
    find ./mobile -type f -exec $SED -i "s/PROJECT_NAME/$PROJECT_NAME/g" {} \;

    echo "[DONE]"
}

function remove_cloned_repo {
    echo -e "\n*** Remove cloned repository ***"

    # Remove cloned repository
    rm -rf ./base_flutter_mvvm

    echo "[DONE]"
}

function install_dependencies {
    echo -e "\n*** Install dependencies ***"

    cd mobile

    # Install dependencies
    flutter pub get

    cd ..

    echo "[DONE]"
}

function add_api_urls_django {
    echo -e "\n*** Add api urls in django ***"

    find ./ -type f -exec $SED -i "s/#path('api\/', include('user.api_urls')),/path('api\/', include('user.api_urls')),/g" {} \;

    echo "[DONE]"
}

function change_flutter_settings {
    echo -e "\n*** Change flutter settings with correct domain names ***"

    LOCAL_URL=`cat docker-compose.yml | grep -w "VIRTUAL_HOST" | $SED -l -i "s/.*=//"`
    DEV_URL=`cat dev.yml | grep -w "VIRTUAL_HOST" | $SED -l -i "s/.*=//"`
    PROD_URL=`cat prod.yml | grep -w "VIRTUAL_HOST" | $SED -l -i "s/.*=//" | $SED -l -i "s/,.*//"`

    $SED -i "s/localhost:8000/$LOCAL_URL/g" ./mobile/lib/settings.dart
    $SED -i "s/forum.deuse.dev/$DEV_URL/g" ./mobile/lib/settings.dart
    $SED -i "s/forum.deuse.live/$PROD_URL/g" ./mobile/lib/settings.dart

    echo "[DONE]"
}

function remove_test_folder {
    echo -e "\n*** Remove test folder ***"

    rm -rf ./mobile/test

    echo "[DONE]"
}

function init_fvm {
    if command -v fvm &> /dev/null
    then
        echo -e "\n*** Init FVM ***"

        cd mobile
        fvm use stable
        cd ..

        echo "[DONE]"
    fi
}

function show_warning_messages {
    echo -e "\n******************** WARNING!!! ********************\n"
    echo -e '''The Flutter base project is now initialized but some settings are still missing and need to be setup manually :\n
        - The internet authorization: add <uses-permission android:name="android.permission.INTERNET"/> in your android/app/src/main/AndroidManifest.xml file.\n
        - The Android and IOS specific setup for the image_picker/url_launcher packages. For those, refer to the documentation in pub.dev website.\n
    '''
    echo -e "\n******************** WARNING!!! ********************\n"
}

# Get project name and domain name
if [ $# -eq  0 ]
then
    read -p 'Project name: ' PROJECT_NAME
    read -p 'Domain name: ' DOMAIN_NAME
elif [ $# -eq  1 ]
then
    read -p 'Domain name: ' DOMAIN_NAME
    PROJECT_NAME=$1
else
    PROJECT_NAME=$1
    DOMAIN_NAME=$2
fi

create_folder
replace_lib
replace_pubspec_analysis_options
replace_with_new_name
install_dependencies
remove_cloned_repo
add_api_urls_django
change_flutter_settings
remove_test_folder
init_fvm
show_warning_messages