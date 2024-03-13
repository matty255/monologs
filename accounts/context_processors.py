def profile_info(request):
    if request.user.is_authenticated:
        user = request.user
        profile_picture = user.profile_picture.url if user.profile_picture else None
        profile_status = user.profile_status
        profile_message = user.profile_message

    else:
        profile_picture = None
        profile_status = None
        profile_message = None

    return {
        "profile_picture": profile_picture,
        "profile_status": profile_status,
        "profile_message": profile_message,
    }
