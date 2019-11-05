from import_export import resources
from .models import ent_cargo

class CargoResource(resources.ModelResource):
    class Meta:
        model = ent_cargo
        fields = ('cargo')