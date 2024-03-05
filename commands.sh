#!/bin/bash

install_initial() {
    python -m venv venv
    source ./venv/Scripts/activate
    pip install django
    while true; do
        echo "Enter additional packages to install (separated by space), or press Enter to skip:"
        read packages
        if [ "$packages" ]; then
            pip install $packages
            pip freeze > requirements.txt
        else
            break
        fi
    done
    while true; do
        echo "Enter admin name:"
        read admin
        django-admin startproject $admin . && break
        echo "Failed to create project. Please try again."
    done
    while true; do
        echo "Enter app name (or 'quit' to stop):"
        read app
        if [ "$app" = "quit" ]; then
            break
        elif [ "$app" ]; then
            python manage.py startapp $app
        fi
    done
}

remove_venv() {
    deactivate
    rm -rf venv
}

# . commands.sh
activate_venv() {
    source ./venv/Scripts/activate
}

add_admin() {
    python manage.py migrate
    python manage.py createsuperuser
}

migrate() {
    python manage.py makemigrations
    python manage.py migrate
}

run() {
    trap 'kill $(jobs -p)' EXIT

    source ./venv/Scripts/activate
    python manage.py runserver &
    python manage.py tailwind start &

    wait
}

create_app() {
    echo "Enter app name:"
    read app
    if [ "$app" ]; then
        python manage.py startapp $app
    fi
}

create_static() {
    mkdir media
    mkdir static
    mkdir templates
}

collectstatic () {
    source ./venv/Scripts/activate
    python manage.py collectstatic
}

reinstall() {
    python -m venv venv
    source ./venv/Scripts/activate
    pip install -r requirements.txt
}

echo "Enter command (install, activate, migrate, run, create, static, reinstall, remove, add_admin):"
read command
case $command in
    "install") install_initial ;;
    "migrate") migrate ;;
    "run") run ;;
    "create") create_app ;;
    "static") create_static ;;
    "reinstall") reinstall ;;
    "remove") remove_venv ;;
    "activate") activate_venv ;;
    "add_admin") add_admin ;;
    "collectstatic") collectstatic ;;
    *) echo "Unknown command" ;;
esac