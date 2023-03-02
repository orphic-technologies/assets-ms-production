from django import forms
from .models import Product, Image


class ProductAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name_of_asset", "supporting_gear", "quantity",
                  "date_of_purchase", "rate_per_unit", "condition_of_asset",
                  "assets_pool", "asset_location",
                  "purpose_of_asset", "date_of_update", "product_category", "vendor", "user"]
        error_messages = {
            "name_of_asset": {"required": "name of asset"},
            "date_of_purchase": {"required": "date of purchase"},
            "supporting_gear": {"required": "supporting gear"},
            "quantity": {"required": "quantity"},
            "rate_per_unit": {"required": "rate"},
            "condition_of_asset": {"required": "condition"},
            "assets_pool": {"required": "asset pool"},
            "asset_location": {"required": "asset location"},
            "purpose_of_asset": {"required": "purpose"},
            "date_of_update": {"required": "date of update"},
            "product_category": {"required": "product category"},
            "vendor": {"required": "vendor name"},
            "user": {"required": " user "},
        }
        widgets = {
            "name_of_asset": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "name of the asset",
                    "id": "validationTooltip01",
                }
            ),
            "rate_per_unit": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "rate",
                    "id": "validationTooltip01",
                }
            ),
            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "quantity",
                    "id": "validationTooltip01",
                }
            ),
            "supporting_gear": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "if any",
                    "id": "validationTooltip01",
                    "rows": "3"
                }
            ),
            "condition_of_asset": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "assets_pool": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "asset_location": forms.Select(
                attrs={
                    "class": "form-select",
                    "placeholder": "location",

                }
            ),
            "purpose_of_asset": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "purpose of asset",
                    "id": "validationTooltip01",
                }
            ),
            "date_of_update": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "date of update",
                }
            ),
            "date_of_purchase": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "date of purchase",
                    "id": "example-date-input",
                }
            ),
            "product_category": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Type the category",
                    "id": "validationTooltip01",
                }
            ),
            "vendor": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "vendor name",
                    "id": "validationTooltip01",
                }
            ),
            "user": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        name_of_asset = self.cleaned_data.get("name_of_asset", None)
        if not name_of_asset:
            print("asset error")
            raise forms.ValidationError(
                "please provide name of the asset", code="invalid")

        quantity = self.cleaned_data.get("quantity", None)
        if not quantity:
            raise forms.ValidationError(
                "provide total quantity of the asset", code="invalid")

        rate_per_unit = self.cleaned_data.get("rate_per_unit", None)
        if not rate_per_unit:
            raise forms.ValidationError(
                "please provide rate of unit of the asset", code="invalid")

        assets_pool = self.cleaned_data.get("assets_pool", None)
        if not assets_pool:
            raise forms.ValidationError(
                "please provide asset-pool of the asset", code="invalid")

        asset_location = self.cleaned_data.get("asset_location", None)
        if not asset_location:
            raise forms.ValidationError(
                "please provide location of the asset", code="invalid")

        purpose_of_asset = self.cleaned_data.get("purpose_of_asset", None)
        if not purpose_of_asset:
            raise forms.ValidationError(
                "please provide purpose of the asset", code="invalid")

        date_of_update = self.cleaned_data.get("date_of_update", None)
        if not date_of_update:
            raise forms.ValidationError(
                "please provide date of update of the product", code="invalid")

        vendor = self.cleaned_data.get("vendor", None)
        if not vendor:
            print("vendor not")
            raise forms.ValidationError(
                "please provide date of update of the product", code="invalid")


class ImageForm(forms.ModelForm):
    images = forms.ImageField(widget=forms.FileInput(
        attrs={"class": "form-control", "multiple": True}), required=False)

    class Meta:
        model = Image
        fields = ['images']
