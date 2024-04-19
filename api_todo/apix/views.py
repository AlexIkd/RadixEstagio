from rest_framework import viewsets
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect

from .forms import CSVUploadForm
import csv

from django.db.models import Avg
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import os

from apix.models import SensorData
from apix.serializers import SensorDataSerial

class SensorViewSet(viewsets.ModelViewSet):
    queryset= SensorData.objects.all()
    serializer_class= SensorDataSerial


def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file= request.FILES['csv_file']
            decoded_file= csv_file.read().decode('utf-8').splitlines()
            csv_reader= csv.DictReader(decoded_file)
            for row in csv_reader:
                SensorData.objects.create(
                    equipment_id=row['equipmentId'],
                    timestamp=row['timestamp'],
                    value=row['value']
            )
            return redirect ('sensordata-list')
    else:
        form = CSVUploadForm()
    return render(request, 'upload_csv.html', {'form': form})


def calcular_media(periodo):
    agora= timezone.now()
    inicio= datetime(1980, 1, 1)
    periodos= {
        'diário': {'inicio': inicio, 'registro': TruncDate('timestamp')},
        'semanal': {'inicio': agora - timedelta(weeks=1), 'registro': TruncWeek('timestamp')},
        'mensal': {'inicio': agora - timedelta(weeks=4), 'registro': TruncMonth('timestamp')}
    }
    if periodo not in periodos:
        raise ValueError("Período inválido")

    inicio = periodos[periodo]['inicio']
    registro = periodos[periodo]['registro']

    sensor_dados = SensorData.objects.filter(timestamp__gte=inicio).annotate(
        periodo_registro=registro
    ).values('periodo_registro').annotate(media=Avg('value'))
    return sensor_dados

def gerar_grafico(request):
    sensores = SensorData.objects.values_list('equipment_id', flat=True).distinct()
    context = {'sensores': sensores}

    # Processo de cálculo e geração de média
    dados_diarios = calcular_media('diário')
    arquivo_grafico_diario = gerar_grafico_medias('diário', dados_diarios)

    dados_semanais = calcular_media('semanal')
    arquivo_grafico_semanal = gerar_grafico_medias('semanal', dados_semanais)

    dados_mensais = calcular_media('mensal')
    arquivo_grafico_mensal = gerar_grafico_medias('mensal', dados_mensais)

    context['arquivo_grafico_diario'] = arquivo_grafico_diario
    context['arquivo_grafico_semanal'] = arquivo_grafico_semanal
    context['arquivo_grafico_mensal'] = arquivo_grafico_mensal

    return render(request, 'carregar_graficos.html', context)

def gerar_grafico_medias(periodo, dados):
    labels = [d['periodo_registro'].strftime('%Y-%m-%d') for d in dados]
    valores = [d['media'] for d in dados]

    plt.bar(labels, valores)
    plt.xlabel('Período')
    plt.ylabel('Valor Médio')
    plt.title(f'Média {periodo.capitalize()} dos Valores do Sensor')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Salvar o gráfico como .png
    nome_arquivo = f'media{periodo}.png'
    caminho_arquivo_static = os.path.join(settings.STATIC_ROOT, nome_arquivo)
    plt.savefig(caminho_arquivo_static)

    # Salvar o gráfico na pasta staticfiles
    caminho_arquivo_staticfiles = os.path.join(settings.STATICFILES_DIRS[0], nome_arquivo)
    plt.savefig(caminho_arquivo_staticfiles)
    plt.close()

    return nome_arquivo

def ver_grafico(request):
    return render(request, 'sensor_media.html')



