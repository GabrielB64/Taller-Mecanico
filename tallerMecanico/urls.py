from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from adminTaller import views


urlpatterns = [
    # Inicio
    path("", views.inicio, name="inicio"),

    # Login
    path("login/admin/", views.login_admin, name="login_admin"),
    path("login/empleado/", views.login_empleado, name="login_empleado"),

    # Django Admin
    path("admin/", admin.site.urls),

    # Dashboard
    path("empleado-dashboard/", views.empleado_dashboard, name="empleado_dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # Trabajos
    path("trabajos/", views.trabajos_lista, name="trabajos_lista"),
    path("trabajos/nuevo/", views.trabajo_crear, name="trabajo_crear"),
    path("trabajos/<int:pk>/", views.trabajo_detalle, name="trabajo_detalle"),
    path("trabajos/<int:pk>/editar/", views.trabajo_editar, name="trabajo_editar"),

    # Empleados
    path("empleados/", views.empleados_lista, name="empleados_lista"),
    path("empleados/nuevo/", views.empleado_crear, name="empleado_crear"),
    path("empleados/<int:pk>/editar/", views.empleado_editar, name="empleado_editar"),
    path("empleados/<int:pk>/eliminar/", views.empleado_eliminar, name="empleado_eliminar"),

    # Herramientas
    path("herramientas/", views.herramientas_lista, name="herramientas_lista"),
    path("herramientas/nuevo/", views.herramienta_crear, name="herramienta_crear"),
    path("herramientas/<int:pk>/editar/", views.herramienta_editar, name="herramienta_editar"),
    path("herramientas/<int:pk>/eliminar/", views.herramienta_eliminar, name="herramienta_eliminar"),

    # Repuestos
    path("repuestos/", views.repuestos_lista, name="repuestos_lista"),
    path("repuestos/nuevo/", views.repuesto_crear, name="repuesto_crear"),
    path("repuestos/<int:pk>/editar/", views.repuesto_editar, name="repuesto_editar"),
    path("repuestos/<int:pk>/eliminar/", views.repuesto_eliminar, name="repuesto_eliminar"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "cambiar-password/",
        views.cambiar_password,
        name="cambiar_password"
    ),
]