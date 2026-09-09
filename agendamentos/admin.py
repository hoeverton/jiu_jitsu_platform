from django.contrib import admin

from .models import (
    Disponibilidade,
    Agendamento,
    Trilha,
    CategoriaTecnica,
    Tecnica,
    TrilhaAluno,
)


@admin.register(Trilha)
class TrilhaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "ordem", "ativa")
    list_filter = ("ativa",)
    search_fields = ("nome",)
    ordering = ("ordem", "nome")


@admin.register(CategoriaTecnica)
class CategoriaTecnicaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "trilha", "ordem", "ativa")
    list_filter = ("trilha", "ativa")
    search_fields = ("nome",)
    ordering = ("trilha", "ordem", "nome")


@admin.register(Tecnica)
class TecnicaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "categoria", "trilha", "ordem", "ativa")
    list_filter = ("trilha", "categoria", "ativa")
    search_fields = ("nome", "descricao")
    ordering = ("trilha", "categoria", "ordem", "nome")

    actions = [
        "mover_para_raspagens",
        "mover_para_guarda",
        "mover_para_passagens",
    ]

    @admin.action(description="Mover selecionadas → Fundamentos / Raspagens")
    def mover_para_raspagens(self, request, queryset):
        try:
            categoria = CategoriaTecnica.objects.get(
                trilha__nome="Fundamentos",
                nome="Raspagens"
            )
        except CategoriaTecnica.DoesNotExist:
            self.message_user(
                request,
                "Categoria Fundamentos → Raspagens não encontrada.",
                level="ERROR"
            )
            return

        quantidade = queryset.update(
            trilha=categoria.trilha,
            categoria=categoria
        )

        self.message_user(
            request,
            f"{quantidade} técnica(s) movida(s) para Fundamentos → Raspagens."
        )

    @admin.action(description="Mover selecionadas → Fundamentos / Guarda")
    def mover_para_guarda(self, request, queryset):
        try:
            categoria = CategoriaTecnica.objects.get(
                trilha__nome="Fundamentos",
                nome="Guarda"
            )
        except CategoriaTecnica.DoesNotExist:
            self.message_user(
                request,
                "Categoria Fundamentos → Guarda não encontrada.",
                level="ERROR"
            )
            return

        quantidade = queryset.update(
            trilha=categoria.trilha,
            categoria=categoria
        )

        self.message_user(
            request,
            f"{quantidade} técnica(s) movida(s) para Fundamentos → Guarda."
        )

    @admin.action(description="Mover selecionadas → Fundamentos / Passagens")
    def mover_para_passagens(self, request, queryset):
        try:
            categoria = CategoriaTecnica.objects.get(
                trilha__nome="Fundamentos",
                nome="Passagens"
            )
        except CategoriaTecnica.DoesNotExist:
            self.message_user(
                request,
                "Categoria Fundamentos → Passagens não encontrada.",
                level="ERROR"
            )
            return

        quantidade = queryset.update(
            trilha=categoria.trilha,
            categoria=categoria
        )

        self.message_user(
            request,
            f"{quantidade} técnica(s) movida(s) para Fundamentos → Passagens."
        )

@admin.register(TrilhaAluno)
class TrilhaAlunoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "aluno",
        "professor",
        "trilha",
        "ativa",
        "criado_em",
        "atualizado_em",
    )

    list_display_links = ("id", "aluno")

    list_filter = (
        "trilha",
        "ativa",
    )

    search_fields = (
        "aluno__username",
        "aluno__email",
        "professor__user__username",
        "trilha__nome",
    )

    ordering = ("-criado_em",)        


admin.site.register(Disponibilidade)
admin.site.register(Agendamento)