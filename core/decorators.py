from django.contrib.auth.decorators import user_passes_test

def es_gestor(user):
    return (user.is_superuser or user.groups.filter(name = "Gestores").exists())

gestor_required = user_passes_test(es_gestor, login_url = "inicio")