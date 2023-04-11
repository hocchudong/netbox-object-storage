from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

try:
    from extras.plugins import PluginMenu
    HAVE_MENU = True
except ImportError:
    HAVE_MENU = False
    PluginMenu = PluginMenuItem

bucket_buttons = [
    PluginMenuButton(
        link='plugins:netbox_object_storage:bucket_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]

cluster_buttons = [
    PluginMenuButton(
        link='plugins:netbox_object_storage:s3cluster_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]

pool_buttons = [
    PluginMenuButton(
        link='plugins:netbox_object_storage:pool_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]


menu_buttons = (
    PluginMenuItem(
        link='plugins:netbox_object_storage:bucket_list',
        link_text='Bucket',
        buttons=bucket_buttons
    ),    
    PluginMenuItem(
        link='plugins:netbox_object_storage:s3cluster_list',
        link_text='S3 Cluster',
        buttons=cluster_buttons
    ),
    PluginMenuItem(
        link='plugins:netbox_object_storage:pool_list',
        link_text='Pool',
        buttons=pool_buttons
    ),
)


if HAVE_MENU:
    menu = PluginMenu(
        label=f'Object Storage',
        groups=(
            ('S3', menu_buttons),
        ),
        icon_class='mdi mdi-clipboard-text-multiple-outline'
    )
else:
    # display under plugins
    menu_items = menu_buttons