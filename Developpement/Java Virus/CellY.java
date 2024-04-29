public class CellY extends Element{
    int immunity=2;
    int round=0;

    public void paralyse(){
        round=3;
    }

    public CellY(int[] pos){
        super.pos=pos;
    }
}