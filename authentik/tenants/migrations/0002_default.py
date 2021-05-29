# Generated by Django 3.2.3 on 2021-05-29 16:55

from django.apps.registry import Apps
from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


def create_default_tenant(apps: Apps, schema_editor: BaseDatabaseSchemaEditor):
    Flow = apps.get_model("authentik_flows", "Flow")
    Tenant = apps.get_model("authentik_tenants", "Tenant")

    db_alias = schema_editor.connection.alias

    default_authentication = (
        Flow.objects.using(db_alias).filter(slug="default-authentication-flow").first()
    )
    default_invalidation = (
        Flow.objects.using(db_alias).filter(slug="default-invalidation-flow").first()
    )

    tenant, _ = Tenant.objects.using(db_alias).update_or_create(
        domain="authentik-default",
        default=True,
        defaults={
            "flow_authentication": default_authentication,
            "flow_invalidation": default_invalidation,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("authentik_tenants", "0001_initial"),
        ("authentik_flows", "0008_default_flows"),
    ]

    operations = [
        migrations.RunPython(create_default_tenant),
    ]
