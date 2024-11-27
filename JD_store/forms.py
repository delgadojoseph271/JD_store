from django import forms
from users.models import User  # Importa el modelo User desde la aplicación 'users'

class RegisterForm(forms.Form): #la calse hereda de Form
    """
    Formulario para el registro de nuevos usuarios.
    """

    # Campo para el nombre de usuario
    username = forms.CharField(
        required=True,
        min_length=4,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'username',
            'placeholder': 'Username'
        })
    )
    
    # Campo para el correo electrónico
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'id': 'email',
            'placeholder': 'example@denmechamba.com'
        })
    )
    
    # Campo para la contraseña
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    
    # Campo para confirmar la contraseña
    password2 = forms.CharField(
        label='Confirmar password',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    
    def clean_username(self):
        """
        Valida que el nombre de usuario no esté en uso.
        Lanza un error si el nombre de usuario ya existe.
        """
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')
        return username
    
    def clean_email(self):
        """
        Valida que el correo electrónico no esté en uso.
        Lanza un error si el correo ya existe.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')
        return email
    
    def clean(self):
        """
        Valida que las contraseñas coincidan.
        Lanza un error si las contraseñas no coinciden.
        """
        cleaned_data = super().clean()
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'El password no coincide')

    def save(self):
        """
        Crea un nuevo usuario con los datos del formulario.
        """
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )
