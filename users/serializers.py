from rest_framework import serializers
from .models import User
import re


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8
    )

    telefone = serializers.CharField(
        required=True,
        write_only=True
    )

    website = serializers.CharField(
        required=False,
        allow_blank=True,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "tipo_usuario",
            "telefone",
            "website",
        ]

    def validate_username(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError(
                "O usuário deve ter pelo menos 3 caracteres."
            )

        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError(
                "Este usuário já está cadastrado."
            )

        return value

    def validate_email(self, value):
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError(
                "Este e-mail já está cadastrado."
            )

        return value

    def validate_tipo_usuario(self, value):
        if value not in ["aluno", "professor"]:
            raise serializers.ValidationError(
                "Tipo de usuário inválido."
            )

        return value

    def validate_password(self, value):
        if value.isdigit():
            raise serializers.ValidationError(
                "A senha não pode conter apenas números."
            )

        return value

    def validate_telefone(self, value):

        # Remove tudo que não for número
        telefone = re.sub(r"\D", "", value)

        # Se o usuário não colocou o código do Brasil,
        # adicionamos 55 automaticamente.
        if telefone.startswith("55"):
            numero = telefone[2:]
        else:
            numero = telefone

        # Celular brasileiro:
        # 2 dígitos de DDD + 9 dígitos
        if len(numero) != 11:
            raise serializers.ValidationError(
                "Digite um WhatsApp válido com DDD."
            )

        # DDD
        ddd = numero[:2]

        # Número celular
        celular = numero[2:]

        # DDD deve possuir 2 dígitos
        if not ddd.isdigit():
            raise serializers.ValidationError(
                "Digite um DDD válido."
            )

        # Celular brasileiro deve começar com 9
        if not celular.startswith("9"):
            raise serializers.ValidationError(
                "Digite um número de celular válido."
            )

        # Salva sempre no formato internacional
        return f"55{numero}"

    def validate_website(self, value):
        if value:
            raise serializers.ValidationError(
                "Não foi possível realizar o cadastro."
            )

        return value

    def create(self, validated_data):

        validated_data.pop("website", None)

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            tipo_usuario=validated_data["tipo_usuario"],
            telefone=validated_data["telefone"],
        )

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "tipo_usuario",
            "telefone",
            "foto",
        ]


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "telefone",
            "foto",
        ]

    def validate_telefone(self, value):

        telefone = re.sub(r"\D", "", value)

        if telefone.startswith("55"):
            numero = telefone[2:]
        else:
            numero = telefone

        if len(numero) != 11:
            raise serializers.ValidationError(
                "Digite um WhatsApp válido com DDD."
            )

        ddd = numero[:2]
        celular = numero[2:]

        if not ddd.isdigit():
            raise serializers.ValidationError(
                "Digite um DDD válido."
            )

        if not celular.startswith("9"):
            raise serializers.ValidationError(
                "Digite um número de celular válido."
            )

        return f"55{numero}"