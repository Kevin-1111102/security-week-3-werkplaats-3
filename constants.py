ROLES = {
    "ervaringsdeskundige",
    "organisatie",
    "admin"
}

USER_ROUTES = {
    "user.dashboard",
    "user.profile",
    "user.update_profile"
}

ORGANIZATION_ROUTES = {
    "organization.dashboard",
    "organization.new_research",
    "organization.update_research"
}

ADMIN_ROUTES = {
    "admin.dashboard",
    "admin.user_detail",
    "admin.research_detail",
    "admin.organization_detail",
    "admin.subscription_detail"
}

RESEARCH_ROUTES = {
    "research.research_details"
}

COMPONENTS_ROUTES = {
    "components.navbar"
}

PROTECTED_API_ROUTES = {
    "api_user.get_all_user",
    "api_user.get_user",
    "api_user.update_user",
    "api_user.delete_user",
    "api_organization.get_all_organization",
    "api_organization.get_organization",
    "api_organization.update_organization",
    "api_organization.delete_organization",
    "api_research.get_all_research",
    "api_research.get_research",
    "api_research.create_research",
    "api_research.update_research",
    "api_research.delete_research",
    "api_disability.get_all_disabilities",
    "api_subscription.get_all_subscription",
    "api_subscription.get_subscription",
    "api_subscription.join_research",
    "api_subscription.withdraw_from_research",
    "api_subscription.update_subscription"
}

PROTECTED_ROUTES = USER_ROUTES | ORGANIZATION_ROUTES | ADMIN_ROUTES | RESEARCH_ROUTES | COMPONENTS_ROUTES | PROTECTED_API_ROUTES