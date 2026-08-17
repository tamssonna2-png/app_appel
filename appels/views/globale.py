from django.shortcuts import render,redirect
from ..forms import EnseignantForm,MatiereForm,EtudiantForm,MotDePasseOblieForm,VerifierCodeForm,NouveauMotDePasseForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Personne,Enseignant,Matiere,Etudiant,FeuilleAppel,Presence,Inscription,Ecole
from django.db.models import Q
from django.shortcuts import get_object_or_404
import re
from urllib.parse import urlparse
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.translation import gettext_lazy as _ #messages.success(request, _("Votre présence a bien été enregistrée.")) comment utiliser
User = get_user_model()

from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def accueil(request):
    if request.user.is_authenticated:
        if hasattr(request.user, 'enseignant'):
            return redirect('dashboard')
        elif hasattr(request.user, 'etudiant'):
            return redirect('dashboard_etudiant')
        return redirect()
    return render(request,'accueil.html')
