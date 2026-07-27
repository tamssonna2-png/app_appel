from django import forms
from .models import Enseignant,Matiere,Etudiant,Ecole

class EnseignantForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Mot de passe"
        )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirmer le mot de passe"
    )

    class Meta:
        model = Enseignant
        fields = ['username','last_name','first_name','email','specialite','telephone','sexe']
        labels = {
            'username':"Nom d'utilisateur (votre identifiant)",
            'last_name':'Nom',
            'first_name':'Prenom',
            'specialite':'Spécialité',
            'sexe':'Sexe'
        } 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        self.fields['sexe'].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm =cleaned_data.get("password_confirm")
        if password and password_confirm:
            if password_confirm != password:
                raise forms.ValidationError("les deux mots de passent ne correspondent pas")
        return cleaned_data

class MatiereForm (forms.ModelForm):
    ecole = forms.CharField(
        label="Ecole",
        widget=forms.TextInput(attrs={
            'list': 'liste-ecoles', 
            'autocomplete': 'off',
            'placeholder': "Tapez pour rechercher un établissement..."
        })
    )
    class Meta:
        model = Matiere
        fields = ['nom','code','credit','description','ecole']#,'est_pondere']
        labels = {
            'nom':"Nom de la matière",
            'code':'Code',
            'credit':'Credit',
            'description':'Description',
            #'ecole':'Ecole'
            #'est_pondere':'Activer la notation par assiduité pour ce cours'
        } 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['nom'].required = True
        self.fields['code'].required = True
        self.fields['credit'].required = True
        """self.fields['ecole'].queryset = Ecole.objects.all().order_by('nom')
        self.fields['ecole'].empty_label = "Selection l'établissement"
        self.fields['ecole'].widget.attrs.update({'id': 'select-ecole'})"""


    def clean_ecole(self):
        """
        Sécurité : L'utilisateur saisit du texte, on doit retrouver l'objet Ecole
        correspondant dans la base de données ou renvoyer une erreur.
        """
        nom_ecole = self.cleaned_data.get('ecole')
        try:
            # On cherche l'école par son nom exact
            ecole_obj = Ecole.objects.get(nom=nom_ecole)
            return ecole_obj
        except Ecole.DoesNotExist:
            raise forms.ValidationError("Cet établissement n'existe pas. Veuillez le sélectionner dans la liste.")
        
class EtudiantForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Mot de passe"
        )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirmer le mot de passe"
    )

    ecole = forms.CharField(
        label="Ecole",
        widget=forms.TextInput(attrs={
            'list': 'liste-ecoles', 
            'autocomplete': 'off',  # Bloque l'historique "uy13" du navigateur
            'placeholder': "Tapez pour rechercher votre établissement..."
        })
    )

    class Meta:
        model = Etudiant
        fields = ['username','last_name','first_name','ecole','email','telephone','sexe']
        labels = {
            'last_name':'Nom',
            'first_name':'Prenom',
            'ecole':'Ecole',
            'username':'Matricule (en magiscule)',
            'sexe':'Sexe'
        } 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].required = True
        self.fields['last_name'].required = True
        self.fields['first_name'].required = True
        self.fields['sexe'].required = True
        self.fields['ecole'].required = True


    
    def clean_ecole(self):
        nom_ecole = self.cleaned_data.get('ecole')
        try:
            return Ecole.objects.get(nom=nom_ecole)
        except Ecole.DoesNotExist:
            raise forms.ValidationError("Cet établissement n'existe pas. Veuillez le sélectionner dans la liste.")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm =cleaned_data.get("password_confirm")
        if password and password_confirm:
            if password_confirm != password:
                raise forms.ValidationError("les deux mots de passent ne correspondent pas")
        return cleaned_data
    def save(self,commit=True):
        etudiant =super().save(commit=False)
        etudiant.set_password(self.cleaned_data["password"])
        etudiant.matricule = self.cleaned_data["username"]
        if commit:
            etudiant.save()
        return etudiant



class MotDePasseOblieForm(forms.Form):
    email = forms.EmailField(
        label='Entrez votre email',
        widget=forms.EmailInput(attrs={'placeholder':'exemple@gmail.com',
        'class':'form-control'})
        )

class VerifierCodeForm(forms.Form):
    code_saisi = forms.CharField(
        label="Code de vérification", 
        max_length=6,
        min_length=6,  # Sécurité : le code fait forcément 6 caractères
        widget=forms.TextInput(attrs={
            'placeholder': '🔏 Ex: 123456', 
            'class': 'form-control text-center fw-bold fs-4',
            'autocomplete': 'off'
        })
    )

from django.core.exceptions import ValidationError

class NouveauMotDePasseForm(forms.Form):
    password = forms.CharField(
        label="Nouveau mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez le nouveau mot de passe'})
    )
    confirm_password = forms.CharField(
        label="Confirmez le mot de passe",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmez le mot de passe'})
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Les deux mots de passe ne correspondent pas.")
        return cleaned_data