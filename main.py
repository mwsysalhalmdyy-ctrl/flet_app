import json
import os
import flet as ft

def main(page: ft.Page):
    # إعدادات شاشة التطبيق
    page.title = "مفردات القرآن الكريم"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.rtl = True  # محاذاة النص للغة العربية من اليمين لليسار
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # تحديد مسار ملف البيانات
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data.json")

    # دالة قراءة البيانات
    def load_data():
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    quran_data = load_data()

    # عناصر الواجهة
    title_text = ft.Text(
        "بحث مفردات القرآن الكريم",
        size=22,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_800,
        text_align=ft.TextAlign.CENTER,
    )

    search_input = ft.TextField(
        label="أدخل اسم السورة أو الكلمة",
        border_radius=10,
        text_align=ft.TextAlign.RIGHT,
    )

    results_list = ft.Column(spacing=10)

    # دالة البحث
    def search_click(e):
        results_list.controls.clear()
        query = search_input.value.strip() if search_input.value else ""

        if not query:
            results_list.controls.append(
                ft.Text("الرجاء إدخل كلمة للبحث", color=ft.Colors.RED_500)
            )
            page.update()
            return

        found = False
        for item in quran_data:
            if query in item["surah"] or query in item["word"]:
                found = True
                card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(f"سورة {item['surah']}", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.GREEN_700),
                                        ft.Text(f"صفحة: {item['page']}", size=14, color=ft.Colors.GREY_700),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                                ft.Divider(),
                                ft.Text(f"المفردة: {item['word']}", size=16, weight=ft.FontWeight.W_500),
                                ft.Text(f"المعنى: {item['meaning']}", size=15, color=ft.Colors.GREY_800),
                            ]
                        ),
                        padding=15,
                    )
                )
                results_list.controls.append(card)

        if not found:
            results_list.controls.append(
                ft.Text("لم يتم العثور على نتائج تطابق بحثك", color=ft.Colors.GREY_600)
            )

        page.update()

    search_button = ft.ElevatedButton(
        content=ft.Text("بحث", size=16),
        icon=ft.Icons.SEARCH,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREEN_600,
            color=ft.Colors.WHITE,
            padding=15,
        ),
        on_click=search_click,
    )

    # إضافة العناصر للشاشة
    page.add(
        title_text,
        ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        search_input,
        ft.Row([search_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20),
        results_list,
    )

# تشغيل التطبيق
ft.app(target=main)