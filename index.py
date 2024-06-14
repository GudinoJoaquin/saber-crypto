import flet as ft

def main(page: ft.Page):
    
    page.title = 'Contador'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    
    txt_number = ft.TextField(value=f'0', text_align=ft.TextAlign.CENTER, width=100)
    
    def menos(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()
        
    def mas(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()
    
    page.add(
        ft.Row(
            [
                ft.IconButton(ft.icons.REMOVE, on_click=menos),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=mas)
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    
    


ft.app(main)