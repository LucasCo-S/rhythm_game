import music

def add_music():
    path_file = "music/"
    path_file += input("Digite o arquivo da musica.\n")
    music.readchart_files(path_file)

def user_input() -> str:
    selected_music: str = input("Digite o nome da musica.\n")
    selected_music += ".txt"

    return selected_music


#add_music()