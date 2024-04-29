import java.util.*;
import java.io.*;

public class Gest {
    int taille;
    ArrayList<ArrayList<Element>> matrix = new ArrayList<ArrayList<Element>>();
    Vector<Element> cellules = new Vector<Element>();
    Vector<Virus> virus = new Vector<Virus>();
    int difficulty;
    int round_game=0;

    public Gest(int taille,int difficulty){
        this.taille = taille;
        this.difficulty=difficulty;
    }


//************************     BOARD      ****************************/

    public void display(int[] pos){

        String line="";
        String line2="";
        String el;
        for(int i=0;i<taille;i++){
            if (i==0){
                line="┌";
            }
            else{
                line="├";
            }
            line2="│";
            for (int j=0;j<taille;j++){
                //determine l'objet représenté
                el=" ";
                if(matrix.get(i).get(j) instanceof CellX){
                    el="\033[1;32mO\033[0m";
                }
                else if(matrix.get(i).get(j) instanceof CellY){
                    el="\033[1;36mO\033[0m";
                }
                else if(matrix.get(i).get(j) instanceof CellZ){
                    el="\033[1;34mO\033[0m";
                }
                else if(matrix.get(i).get(j) instanceof Virus){
                    el="\033[1;31m¤\033[0m";
                }

                //Créer les lignes à afficher successivement pour obtenir la grille
                if (j<taille-1){
                    //ligne supérieur
                    if (i==0){
                        line+="─────┬";
                    }
                    else{
                        if (i==pos[0] && j==pos[1]){
                            line+="──1──┼";
                        }
                        else if(i==pos[0] && j==pos[1]-1){
                            line+="─────┼";
                        }
                        else if(i==pos[0]+1 && j==pos[1]){
                            line+="──3──┼";
                        }
                        else{
                            line+="─────┼";}
                        }
                    //Ligne inferieur contenant l'objet
                    if (i==pos[0] && j==pos[1]){
                        line2+="  "+el+"  2";
                    }
                    else if(i==pos[0] && j==pos[1]-1){
                        line2+="  "+el+"  4";
                    }
                    else if(i==pos[0]+1 && j==pos[1]){
                        line2+="  "+el+"  │";
                    }
                    else{
                    line2+="  "+el+"  │";}}
                    //Fin de ligne
                    else{
                        if(i==0){
                            line+="─────┐";
                            }
                        else{
                            if (i==pos[0] && j==pos[1]){
                                line+="──1──┤";
                            }
                            else if(i==pos[0] && j==pos[1]-1){
                                line+="─────┤";
                            }
                            else if(i==pos[0]+1 && j==pos[1]){
                                line+="──3──┤";
                            }
                            else{
                                line+="─────┤";}
                            }
                        line2+="  "+el+"  │";
                    }
                }

            System.out.println(line+"\n"+line2);
            }
            //Fin de colonne
            line="└";
            for (int j=0;j<taille;j++){
                if(j<taille-1){
                    line+="─────┴";}
                else{
                    line+="─────┘";
                }

            }
            System.out.println(line);

    }


    public void init(){
        boolean test=true;

        for(int i =0;i<taille;i++){
            matrix.add(new ArrayList<Element>());
        }
        for (int i=0;i<taille;i++){
            for(int j=0;j<taille;j++){
            matrix.get(i).add(null);}
        }

        for(int i=0;i<10;i++){
            test=true;
            while(test){
                int[] randV={(int) (Math.random()*taille),(int) (Math.random()*taille)};
                if(matrix.get(randV[0]).get(randV[1])==null){
                test=false;
                Virus vir = new Virus(randV);
                virus.add(vir);
                matrix.get(randV[0]).set(randV[1],vir);}}}


        for(int i=0;i<45;i++){
            if (i%(4-difficulty)==0){
                test=true;
                while(test){
                    int[] randX={(int) (Math.random()*taille),(int) (Math.random()*taille)};
                    if(matrix.get(randX[0]).get(randX[1])==null){
                        test=false;
                        CellX cellx = new CellX(randX);
                        cellules.add(cellx);
                        matrix.get(randX[0]).set(randX[1],cellx);}}}

            test=true;
            while(test){
                int[] randY={(int) (Math.random()*taille),(int) (Math.random()*taille)};
                if(matrix.get(randY[0]).get(randY[1])==null){
                    test=false;
                    CellY celly = new CellY(randY);
                    cellules.add(celly);
                    matrix.get(randY[0]).set(randY[1],celly);}}

            if (i%difficulty==0){
                test=true;
                while(test){
                    int[] randZ={(int) (Math.random()*taille),(int) (Math.random()*taille)};
                    if(matrix.get(randZ[0]).get(randZ[1])==null){
                        test=false;
                        CellZ cellz = new CellZ(randZ);
                        cellules.add(cellz);
                        matrix.get(randZ[0]).set(randZ[1],cellz);}}}
                    }}
    

    public ArrayList<Element> getadjacent(int[] pos){
        ArrayList<Element> adj = new ArrayList<Element>();
        //4
        if(pos[0]==0){
            adj.add(new Mur());
        }else{
        adj.add(matrix.get(pos[0]-1).get(pos[1]));}
        //3
        if(pos[1]==19){
            adj.add(new Mur());
        }else{
        adj.add(matrix.get(pos[0]).get(pos[1]+1));}
        //2
        if(pos[0]==19){
            adj.add(new Mur());
        }else{
        adj.add(matrix.get(pos[0]+1).get(pos[1]));}
        //1
        if(pos[1]==0){
            adj.add(new Mur());
        }else{
        adj.add(matrix.get(pos[0]).get(pos[1]-1));}
        return adj;
    }



//***************************    ACTION       *******************************/



    public boolean moveVirus(Element el,ArrayList<Element> adj,int choice){
        int[] posel = {el.pos[0],el.pos[1]};
        int[] posadj={0,0};
        if (adj.get(choice-1) != null){
        posadj = adj.get(choice-1).pos;}
        if (adj.get(choice-1) instanceof CellX){
            for(int i=0;i<cellules.size();i++){if(cellules.get(i)==adj.get(choice-1)){cellules.remove(i);}} //remove adj dans vector
            matrix.get(posadj[0]).set(posadj[1],el); //poser element à pos adj 
            matrix.get(posel[0]).set(posel[1],null);//poser null à ancienne position
            el.pos=posadj;
            el.round+=1;
            System.out.println(Arrays.toString(el.pos));
            return false;
        }
        if (adj.get(choice-1) instanceof CellY){
            adj.get(choice-1).paralyse(); //Paralyser cellule
            el.round+=1;
            System.out.println(Arrays.toString(el.pos));
            return false;
        }
        if (adj.get(choice-1) instanceof CellZ || adj.get(choice-1) instanceof Virus || adj.get(choice-1) instanceof Mur){
            System.out.println("Déplacement impossible,réessayez");
            return true;
        }
        if (adj.get(choice-1) == null){
            if(choice==1){matrix.get(posel[0]-1).set(posel[1],el);el.pos[0]=posel[0]-1;el.pos[1]=posel[1];}
            if(choice==2){matrix.get(posel[0]).set(posel[1]+1,el);el.pos[0]=posel[0];el.pos[1]=posel[1]+1;}
            if(choice==3){matrix.get(posel[0]+1).set(posel[1],el);el.pos[0]=posel[0]+1;el.pos[1]=posel[1];}
            if(choice==4){matrix.get(posel[0]).set(posel[1]-1,el);el.pos[0]=posel[0]-1;el.pos[1]=posel[1]-1;} //poser element à pos adj 
            matrix.get(posel[0]).set(posel[1],null);//poser null à ancienne position
            return false;
        }
        return true;
        }

    public boolean moveCell(Element el,ArrayList<Element> adj,int choice){
        System.out.println(adj.get(choice-1));
        int[] posel = {el.pos[0],el.pos[1]};
        int[] posadj={0,0};
        if (adj.get(choice-1) != null){
        posadj = adj.get(choice-1).pos;}
        if (adj.get(choice-1) instanceof CellX || adj.get(choice-1) instanceof CellY || adj.get(choice-1) instanceof CellZ){
            if(el.immunity<adj.get(choice-1).immunity){
            for(int i=0;i<cellules.size();i++){if(cellules.get(i)==adj.get(choice-1)){cellules.remove(i);}}//remove la cellule à l'immunité la plus forte dans la liste cellules
            matrix.get(posadj[0]).set(posadj[1],null);
            el.pos=posadj;}//set null à l'ancienne position
            else{//compare les deux immunités -> supprimer cellule à l'immunité la plus élevé (el)
            for(int i=0;i<cellules.size();i++){if(cellules.get(i)==el){cellules.remove(i);}}//remove la cellule à l'immunité la plus forte dans la liste cellules
            matrix.get(posel[0]).set(posel[1],null);
            el.pos=posel;}//set null à l'ancienne position
            return false;
        }
        if (adj.get(choice-1) instanceof Virus || adj.get(choice-1) instanceof Mur){
            return true;
        }
        if (adj.get(choice-1) == null){
            if(choice==1){matrix.get(posel[0]-1).set(posel[1],el);el.pos[0]=posel[0]-1;el.pos[1]=posel[1];}
            if(choice==2){matrix.get(posel[0]).set(posel[1]+1,el);el.pos[0]=posel[0];el.pos[1]=posel[1]+1;}
            if(choice==3){matrix.get(posel[0]+1).set(posel[1],el);el.pos[0]=posel[0]+1;el.pos[1]=posel[1];}
            if(choice==4){matrix.get(posel[0]).set(posel[1]-1,el);el.pos[0]=posel[0]-1;el.pos[1]=posel[1]-1;} //poser element à pos adj 
            matrix.get(posel[0]).set(posel[1],null);//poser null à ancienne position
            return false;
        }
    return true;
    }

    
    public void split(Element el){
        ArrayList<Element> adj = getadjacent(el.pos);//verfier case adjacente
        Virus vir;
        for (int i = 0;i<adj.size();i++){
        if(adj.get(i)==null){switch(i){
            case 1:int[] pos1={el.pos[0],el.pos[1]};vir=new Virus(pos1);virus.add(vir);
            matrix.get(el.pos[0]-1).set(el.pos[1],vir);break;
            case 2:int[] pos2={el.pos[0]+1,el.pos[1]};vir=new Virus(pos2);virus.add(vir);
            matrix.get(el.pos[0]).set(el.pos[1]+1,vir);break;
            case 3:int[] pos3={el.pos[0],el.pos[1]+1};vir=new Virus(pos3);virus.add(vir);
            matrix.get(el.pos[0]+1).set(el.pos[1],vir);break;
            case 4:int[] pos4={el.pos[0]-1,el.pos[1]};vir=new Virus(pos4);virus.add(vir);
            matrix.get(el.pos[0]).set(el.pos[1]-1,vir);break;
        }}}//poser new virus sur case adjacente
    }


//**********************    MENU           *********************/

    public void menu() {
        System.out.println("menu");
        
        System.out.println("Bienvenue dans le virus Game \n");
        System.out.println("Que voulez-vous faire ?");
        // System.out.println("1 \t Jouer à deux");
        System.out.println("2 \t Jouer contre l'ordinateur");
        System.out.println("3 \t Afficher les règles");
        System.out.println("0 \t Quitter le jeu");
        int choice = saisieEntier();
        
        switch(choice){
            case 2:this.play();break;
            case 3:this.rules();break;
            case 4:System.exit(0);
        }
    }

    public void play(){
        System.out.println("play");
        while(true){
            for (int i=0; i<virus.size(); i++) {
                // this.display(virus.get(i).pos);
                this.deplacement(virus.get(i));
                virus.get(i).round-=1;
            }
            for (int i=0; i<4; i++) {
                int num= (int)Math.random()*cellules.size();
                // this.display(cellules.get(num).pos);
                if(cellules.get(num) instanceof CellY){if(cellules.get(num).round>0){continue;}
                this.deplacement(cellules.get(num));
                cellules.get(num).round-=1;}
            }
            round_game += 1;
            if(round_game%10==0 && round_game!=0){int size=virus.size();
            for (int i=0; i<size;i++){this.split(virus.get(i));}}
            this.checkVictory();
            
        }
    }

    public void deplacement(Element el){
        boolean test=true;
        this.display(el.pos);
        while(test){
        if(el instanceof Virus){
            
            System.out.println("C'est au tour des virus! \n Que voulez-vous faire ?");
            System.out.println("Vous pouvez vous déplacer en saisissant le chiffre correspondant à la direction\n");
            System.out.println("1: haut");
            System.out.println("2: droite");
            System.out.println("3: bas");
            System.out.println("4: gauche");
            int direction = saisieEntier();
            
            test=this.moveVirus(el,this.getadjacent(el.pos),direction);}
        else{
            test=this.moveCell(el,this.getadjacent(el.pos),(int)(Math.random()*4));
        }
    }
}

    public void rules(){
        System.out.println("The Rules !!!");
    }

    public void checkVictory() {
        if (cellules.isEmpty()) {
            System.out.println("Vous avez gagné \n");
        }
        else if (virus.isEmpty()) {
            System.out.println("Vous avez perdu \n");
        }
        else{
            return;
        }
        // lance fin du jeu + message
        System.out.println("Fin du jeu");
        // retourne à combien de tour gagné ou perdu
        System.out.println("Vous avez fini le jeu au bout de " + round_game);
        System.exit(0);
    } 


//**********************    MISC       ************************/

    public static int saisieEntier () //Permet de pouvoir insérer un entier
    {
        while (true)
        {
            try
            {
                BufferedReader buff = new BufferedReader(new InputStreamReader(System.in));
                String chaine=buff.readLine();
                int num = Integer.valueOf(chaine).intValue();
                return num;
            }
            catch(NumberFormatException e) 
            {
                System.out.println("Erreur de saisie recommencez");
            }
            catch(IOException e) 
            {
                System.out.println(" Impossible de travailler" +e);
                return 0;
            }  
        }
    }

    public static void main(String[] args){

        Gest table = new Gest(20,1);
        table.init();
        table.menu();
    }
}

