import java.util.*;

import java.io.*;
import java.nio.*;


public class Main {
    public static void main(String[] args)
    {
        affiche_menu();
        int reponse = saisieEntier();

        switch (reponse) //Relie la saisie de l'entier avec les classes
        {
            case 1: System.out.println("vous pouvez jouer");break;
        }
    }
}