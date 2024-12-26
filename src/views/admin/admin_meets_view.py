import flet as ft, asyncio
from flet_navigator import PageData
from components.loader import Loader

def admin_meets_screen(page_data: PageData):
	global rows
	page = page_data.page
	rows = []

	async def on_mount():
		global rows 
		loader = Loader(page)
		asyncio.create_task(loader.create_loader())
		# meets_data = await handle_get_all_valid_meets()
		loader.delete_loader()

	return ft.Container()
		
		