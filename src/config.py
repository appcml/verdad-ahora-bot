#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

# Facebook Config
FB_PAGE_ID = os.getenv('FB_PAGE_ID')
FB_ACCESS_TOKEN = os.getenv('FB_ACCESS_TOKEN')

# APIs (opcional pero recomendado)
NEWS_API_KEY = os.getenv('NEWS_API_KEY')  # newsapi.org
GNEWS_API_KEY = os.getenv('GNEWS_API_KEY')  # gnews.io

# Páginas de referencia para analizar estilo
PAGINAS_REFERENCIA = [
    {
        'nombre': 'El Oso Video',
        'url': 'https://www.facebook.com/elosovideo',
        'tipo': 'humor_sátira_política',
        'tono': 'irónico',
        'engagement': 'alto'
    },
    {
        'nombre': 'Soy Código',
        'url': 'https://www.facebook.com/soycodigo', 
        'tipo': 'tecnología_programación',
        'tono': 'educativo_divertido',
        'engagement': 'medio'
    },
    {
        'nombre': 'Rosario Tres',
        'url': 'https://www.facebook.com/Rosariotres',
        'tipo': 'noticias_locales',
        'tono': 'informativo_urgente',
        'engagement': 'alto'
    },
    {
        'nombre': 'Rab Garmon',
        'url': 'https://www.facebook.com/RabGarmon',
        'tipo': 'opinión_política',
        'tono': 'crítico_directo',
        'engagement': 'muy_alto'
    },
    {
        'nombre': 'Perfil 61556345831824',
        'url': 'https://www.facebook.com/profile.php?id=61556345831824',
        'tipo': 'viral_entretenimiento',
        'tono': 'sensacionalista',
        'engagement': 'alto'
    },
    {
        'nombre': 'Perfil 61577013128003',
        'url': 'https://www.facebook.com/profile.php?id=61577013128003',
        'tipo': 'noticias_internacionales',
        'tono': 'dramático',
        'engagement': 'medio'
    },
    {
        'nombre': 'Perfil 61581173565137',
        'url': 'https://www.facebook.com/profile.php?id=61581173565137',
        'tipo': 'conspiraciones_misterio',
        'tono': 'intrigante',
        'engagement': 'muy_alto'
    }
]

# Fuentes de noticias confiables para obtener datos reales
FUENTES_NOTICIAS = {
    'tecnologia': [
        'https://feeds.bbci.co.uk/news/technology/rss.xml',
        'https://www.xataka.com/rss.xml',
        'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/tecnologia/portada',
    ],
    'internacional': [
        'https://feeds.bbci.co.uk/news/world/rss.xml',
        'https://rss.cnn.com/rss/edition_world.rss',
        'https://www.france24.com/es/rss',
    ],
    'politica': [
        'https://feeds.elpais.com/mrss-s/pages/ep/site/elpais.com/section/internacional/portada',
        'https://elmundo.es/rss/portada.xml',
    ],
    'viral': [
        'https://news.google.com/rss?hl=es&gl=ES&ceid=ES:es',
    ]
}

# Templates de engagement aprendidos de las páginas de referencia
TEMPLATES_ENGAGEMENT = {
    'hook_inicial': [
        "🚨 ATENCIÓN: {titulo}",
        "😱 NO LO VAS A CREER: {titulo}",
        "🔥 ESTO EXPLOTA AHORA: {titulo}",
        "⚠️ ÚLTIMA HORA: {titulo}",
        "🤯 REVELAN: {titulo}",
        "💥 POLÉMICA: {titulo}",
        "👀 MIRA ESTO: {titulo}",
        "🛑 ALERTA: {titulo}",
    ],
    'cuerpo_estilos': {
        'ironico': [
            "Mientras tanto en el mundo... {contenido}",
            "Y pensar que algunos todavía creen que... {contenido}",
            "La ironía del día: {contenido}",
        ],
        'urgente': [
            "Información en desarrollo: {contenido}",
            "Detalles que están saliendo a la luz: {contenido}",
            "Lo que sabemos hasta ahora: {contenido}",
        ],
        'intrigante': [
            "Hay algo que no cuadra... {contenido}",
            "Las piezas empiezan a encajar: {contenido}",
            "Lo que no te cuentan: {contenido}",
        ],
        'critico': [
            "La realidad que enfrentamos: {contenido}",
            "Sin filtros: {contenido}",
            "La verdad incómoda: {contenido}",
        ]
    },
    'llamada_accion': [
        "\n\n💬 ¿Qué opinas? Comenta 👇",
        "\n\n🔁 Comparte si estás de acuerdo",
        "\n\n👍 Dale like si te sorprendió",
        "\n\n💭 Tu opinión cuenta - Comenta",
        "\n\n🚨 Difunde esta información",
        "\n\n👉 Síguenos para más contenido así",
    ]
}

# Configuración de imágenes
IMAGEN_CONFIG = {
    'width': 1200,
    'height': 630,
    'colores_virales': [
        '#FF0000',  # Rojo urgente
        '#FF6B00',  # Naranja alerta
        '#FFD700',  # Amarillo atención
        '#1DA1F2',  # Azul confianza
        '#000000',  # Negro misterio
        '#FF1493',  # Rosa impactante
    ],
    'fuentes_titulo': [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
    ]
}

TIEMPO_ENTRE_PUBLICACIONES = 60  # minutos
