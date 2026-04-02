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
    class Meta:
        model = Matiere
        fields = ['nom','code','credit','description','ecole']#,'est_pondere']
        labels = {
            'nom':"Nom de la matière",
            'code':'Code',
            'credit':'Credit',
            'description':'Description',
            'ecole':'Ecole'
            #'est_pondere':'Activer la notation par assiduité pour ce cours'
        } 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['nom'].required = True
        self.fields['code'].required = True
        self.fields['credit'].required = True
        self.fields['ecole'].queryset = Ecole.objects.all().order_by('nom')
        self.fields['ecole'].empty_label = "Selection l'établissement"
        
class EtudiantForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label="Mot de passe"
        )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirmer le mot de passe"
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