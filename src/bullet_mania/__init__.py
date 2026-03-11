from bullet_mania.game import run
from bullet_mania.levelEditor import run_editor

def main() -> None:
    print("BULLET MANIA")
    print("Scegli modalità di esecuzione :")
    print("\n1) Gioca come Client")
    print("2) Gioca come Host")
    print("3) Apri Level Editor\n")

    run_mode = int(input("Inserisci modalità di esecuzione : "))
    while run_mode not in [1, 2, 3]:
        print("Modalità di esecuzione non valida. Riprova.")
        run_mode = int(input("Inserisci modalità di esecuzione : "))

    if run_mode == 1:
        run()
    elif run_mode == 2:
        pass
    elif run_mode == 3:
        run_editor()

if __name__ == "__main__":
    main()
