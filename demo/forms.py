from demo.models import User, Application
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class RegisterUserForm(forms.ModelForm):
    name = forms.CharField(label='Имя', validators=[RegexValidator('^[а-яА-Я ]+$',
                                                                   message='Разрешены только кириллица, тире или пробел!')],
                           error_messages={
                               'required': 'Обязательное поле'
                           })
    surname = forms.CharField(label='Фамилия', validators=[RegexValidator('^[а-яА-Я ]+$',
                                                                          message='Разрешены только кириллица, тире или пробел!')],
                              error_messages={
                                  'required': 'Обязательное поле'
                              })
    patronymic = forms.CharField(label='Отчество', validators=[RegexValidator('^[а-яА-Я ]+$',
                                                                              message='Разрешены только кириллица, тире или пробел!')],
                                 required=False)
    username = forms.CharField(label='Логин', validators=[RegexValidator('^[a-zA-Z ]+$',
                                                                         message='Разрешены только латиница, тире или пробел!')],
                               error_messages={
                                   'required': 'Обязательное поле',
                                   'unique': 'Данный логин уже занят!',
                               })
    email = forms.EmailField(label='Почта',
                             error_messages={
                                 'required': 'Обязательное поле',
                                 'unique': 'Данная почта уже занята!',
                             })
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput, min_length=6,
                                error_messages={
                                    'required': 'Обязательное поле',
                                })
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput, min_length=6,
                                error_messages={
                                    'required': 'Обязательное поле',
                                })
    role = forms.BooleanField(label='Согласен(на) на условия использования данных!', required=True, widget=forms.CheckboxInput)

    def clean_password2(self):
        # Проверьте, что два пароля совпадают
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        # Сохранить предоставленный пароль в хэшированном формате
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('name', 'surname', 'patronymic', 'username', 'email', 'password1', 'password2', 'role')


class ApplicationForm(forms.ModelForm):
    name = forms.CharField(label='Имя', validators=[RegexValidator('^[а-яА-Я ]+$',
                                                                   message='Разрешены только кириллица, тире или пробел!')],
                           error_messages={
                               'required': 'Обязательное поле'
                           })
    phone = forms.CharField(label='Телефон', min_length=11)
    email = forms.EmailField(label='Почта',
                             error_messages={
                                 'required': 'Обязательное поле',
                                 'unique': 'Данная почта уже занята!',
                             })

    class Meta:
        model = Application
        fields = ['name', 'phone', 'email']
