from Image_library.images import get_champion_icon, get_item_icon

def main():
        item_icon = get_item_icon(3340)
        champion_icon = get_champion_icon(62)

        print("Item icon result:", item_icon if item_icon else "Item not found")
        print("Champion icon result:", champion_icon if champion_icon else "Champion not found")

if __name__ == "__main__":
    main()
 