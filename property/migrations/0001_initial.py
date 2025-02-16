# Generated by Django 5.1.5 on 2025-02-06 18:01

import django.db.models.deletion
import property.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Property",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=255, null=True, unique=True
                    ),
                ),
                ("contact_phone", models.CharField(max_length=20)),
                (
                    "description",
                    models.TextField(blank=True, max_length=1000, null=True),
                ),
                ("location", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "latitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                (
                    "longitude",
                    models.DecimalField(
                        blank=True, decimal_places=6, max_digits=9, null=True
                    ),
                ),
                ("country", models.CharField(blank=True, max_length=100, null=True)),
                ("state", models.CharField(blank=True, max_length=100, null=True)),
                ("district", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "subdivision",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("village", models.CharField(blank=True, max_length=100, null=True)),
                ("pincode", models.CharField(blank=True, max_length=10, null=True)),
                (
                    "deal_type",
                    models.CharField(
                        choices=[
                            ("SELL", "Sell"),
                            ("BUY", "Buy"),
                            ("RENT", "Rent"),
                            ("LEASE", "Lease"),
                            ("SHORT_TERM_RENT", "Rent Out (Short-Term)"),
                            ("AUCTION", "Auction"),
                            ("EXCHANGE", "Exchange"),
                            ("INVEST", "Invest"),
                            ("CO_OWN", "Co-Own"),
                            ("PRE_SALE", "Pre-Sale/Under Construction"),
                            ("PG_HOSTEL", "PG/Hostel"),
                            ("COMMERCIAL", "Commercial Use"),
                            ("AGRICULTURAL", "Agricultural/Farm Land"),
                            ("VACATION_HOME", "Vacation Home"),
                            ("FORECLOSURE", "Foreclosure/Distressed Properties"),
                            ("CO_LIVING", "Co-Living Spaces"),
                        ],
                        default="SELL",
                        max_length=50,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("AVAILABLE", "Available"),
                            ("PENDING", "Pending"),
                            ("SOLD", "Sold"),
                            ("RENTED", "Rented"),
                            ("CLOSED", "Closed"),
                        ],
                        default="AVAILABLE",
                        max_length=50,
                    ),
                ),
                ("listing_date", models.DateField(auto_now_add=True, null=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                ("is_published", models.BooleanField(default=True)),
                ("featured", models.BooleanField(default=False)),
                (
                    "contact_email",
                    models.EmailField(blank=True, max_length=254, null=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="properties",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-listing_date"],
            },
        ),
        migrations.CreateModel(
            name="PropertyUserTrack",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user_email",
                    models.EmailField(
                        help_text="Email of the authenticated user.",
                        max_length=254,
                        unique=True,
                    ),
                ),
                (
                    "property_like",
                    models.JSONField(
                        default=list,
                        help_text="List of Property IDs liked by the user.",
                    ),
                ),
                (
                    "property_share",
                    models.JSONField(
                        default=list,
                        help_text="List of Property IDs shared by the user.",
                    ),
                ),
                (
                    "property_view",
                    models.JSONField(
                        default=list,
                        help_text="List of Property IDs viewed by the user.",
                    ),
                ),
                (
                    "property_comment",
                    models.JSONField(
                        default=list,
                        help_text="List of Property IDs commented by the user.",
                    ),
                ),
                (
                    "property_report",
                    models.JSONField(
                        default=list,
                        help_text="List of Property IDs reported by the user.",
                    ),
                ),
                (
                    "property_favourite",
                    models.JSONField(
                        default=list,
                        help_text="List of Property IDs marked as favourites by the user.",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="CommercialProperty",
            fields=[
                (
                    "property_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="property.property",
                    ),
                ),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("SHOP", "Shop"),
                            ("OFFICE_SPACE", "Office Space"),
                            ("WAREHOUSE", "Warehouse"),
                            ("COMMERCIAL_PROPERTY", "Commercial Property"),
                        ],
                        default="SHOP",
                        max_length=50,
                    ),
                ),
                (
                    "area",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "furnishing_status",
                    models.CharField(
                        choices=[
                            ("FURNISHED", "Furnished"),
                            ("SEMI_FURNISHED", "Semi-Furnished"),
                            ("UNFURNISHED", "Unfurnished"),
                        ],
                        default="UNFURNISHED",
                        max_length=20,
                    ),
                ),
                (
                    "parking",
                    models.CharField(
                        choices=[
                            ("NONE", "No Parking"),
                            ("COVERED", "Covered Parking"),
                            ("OPEN", "Open Parking"),
                        ],
                        default="NONE",
                        max_length=20,
                    ),
                ),
                ("year_built", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ("total_floors", models.PositiveIntegerField(blank=True, null=True)),
                ("floor_number", models.PositiveIntegerField(blank=True, null=True)),
                ("has_air_conditioning", models.BooleanField(default=False)),
                ("has_elevator", models.BooleanField(default=False)),
                ("is_renovated", models.BooleanField(default=False)),
            ],
            bases=("property.property",),
        ),
        migrations.CreateModel(
            name="IndustrialProperty",
            fields=[
                (
                    "property_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="property.property",
                    ),
                ),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("INDUSTRIAL_PROPERTY", "Industrial Property"),
                            ("BUILDING", "Building"),
                        ],
                        default="INDUSTRIAL_PROPERTY",
                        max_length=50,
                    ),
                ),
                (
                    "area",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "furnishing_status",
                    models.CharField(
                        choices=[
                            ("FURNISHED", "Furnished"),
                            ("SEMI_FURNISHED", "Semi-Furnished"),
                            ("UNFURNISHED", "Unfurnished"),
                        ],
                        default="UNFURNISHED",
                        max_length=20,
                    ),
                ),
                (
                    "parking",
                    models.CharField(
                        choices=[
                            ("NONE", "No Parking"),
                            ("COVERED", "Covered Parking"),
                            ("OPEN", "Open Parking"),
                        ],
                        default="NONE",
                        max_length=20,
                    ),
                ),
                ("year_built", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
                ("total_floors", models.PositiveIntegerField(blank=True, null=True)),
                ("floor_number", models.PositiveIntegerField(blank=True, null=True)),
                ("has_lift", models.BooleanField(default=False)),
                ("has_security", models.BooleanField(default=False)),
            ],
            bases=("property.property",),
        ),
        migrations.CreateModel(
            name="LandProperty",
            fields=[
                (
                    "property_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="property.property",
                    ),
                ),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("LAND", "Land"),
                            ("PLOT", "Plot"),
                            ("FARM_LAND", "Farm Land"),
                        ],
                        default="LAND",
                        max_length=50,
                    ),
                ),
                (
                    "total_area",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "area_unit",
                    models.CharField(
                        choices=[
                            ("SQFT", "Square Feet"),
                            ("ACRES", "Acres"),
                            ("HECTARES", "Hectares"),
                            ("SQM", "Square Meters"),
                        ],
                        default="SQFT",
                        max_length=10,
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=15, null=True
                    ),
                ),
                (
                    "nearby_amenities",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("nearby", models.CharField(blank=True, max_length=500, null=True)),
                (
                    "distance_from_road",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("has_water", models.BooleanField(default=False)),
                ("has_electricity", models.BooleanField(default=False)),
                ("is_corner_plot", models.BooleanField(default=False)),
                ("soil_type", models.CharField(blank=True, max_length=100, null=True)),
                ("irrigation_facilities", models.BooleanField(default=False)),
                (
                    "facing",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("NORTH", "North"),
                            ("SOUTH", "South"),
                            ("EAST", "East"),
                            ("WEST", "West"),
                            ("NORTH_EAST", "North-East"),
                            ("NORTH_WEST", "North-West"),
                            ("SOUTH_EAST", "South-East"),
                            ("SOUTH_WEST", "South-West"),
                        ],
                        max_length=50,
                        null=True,
                    ),
                ),
            ],
            bases=("property.property",),
        ),
        migrations.CreateModel(
            name="ResidentialProperty",
            fields=[
                (
                    "property_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="property.property",
                    ),
                ),
                (
                    "property_type",
                    models.CharField(
                        choices=[
                            ("HOUSE", "House"),
                            ("APARTMENT", "Apartment"),
                            ("VILLA", "Villa"),
                            ("BUNGALOW", "Bungalow"),
                            ("RESORT_PROPERTY", "Resort Property"),
                            ("FARM_HOUSE", "Farm House"),
                        ],
                        default="HOUSE",
                        max_length=50,
                    ),
                ),
                ("bedrooms", models.PositiveIntegerField(blank=True, null=True)),
                ("bathrooms", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "furnishing_status",
                    models.CharField(
                        choices=[
                            ("FURNISHED", "Furnished"),
                            ("SEMI_FURNISHED", "Semi-Furnished"),
                            ("UNFURNISHED", "Unfurnished"),
                        ],
                        default="UNFURNISHED",
                        max_length=20,
                    ),
                ),
                (
                    "parking",
                    models.CharField(
                        choices=[
                            ("NONE", "No Parking"),
                            ("COVERED", "Covered Parking"),
                            ("OPEN", "Open Parking"),
                        ],
                        default="NONE",
                        max_length=20,
                    ),
                ),
                (
                    "built_up_area",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("total_floors", models.PositiveIntegerField(blank=True, null=True)),
                ("floor_number", models.PositiveIntegerField(blank=True, null=True)),
                ("balcony_count", models.PositiveIntegerField(blank=True, null=True)),
                ("has_garden", models.BooleanField(default=False)),
                ("has_pool", models.BooleanField(default=False)),
                ("year_built", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=12, null=True
                    ),
                ),
            ],
            bases=("property.property",),
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.CharField(blank=True, default="guest", max_length=100)),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="replies",
                        to="property.comment",
                    ),
                ),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="propertycomments",
                        to="property.property",
                    ),
                ),
            ],
            options={
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="PropertyActions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "activity_counts",
                    models.JSONField(
                        default=dict,
                        help_text="Nested structure to store activity counts for authenticated users and guests.",
                    ),
                ),
                (
                    "property",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="actions",
                        to="property.property",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PropertyDocument",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "document",
                    models.FileField(upload_to=property.models.dynamic_file_upload),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="documents",
                        to="property.property",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PropertyImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(upload_to=property.models.dynamic_file_upload),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="property.property",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PropertyVideo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "video",
                    models.FileField(upload_to=property.models.dynamic_file_upload),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "property",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="videos",
                        to="property.property",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.CharField(blank=True, max_length=150, null=True)),
                (
                    "report_type",
                    models.CharField(
                        choices=[
                            ("spam", "Spam"),
                            ("expired", "Expired"),
                            ("no_response", "No Response"),
                            ("other", "Other"),
                        ],
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "additional_info",
                    models.TextField(
                        blank=True,
                        help_text="Additional information about the report.",
                        null=True,
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reports",
                        to="property.property",
                    ),
                ),
            ],
        ),
    ]
