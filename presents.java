
import java.util.Scanner;

public class presents
{
    public static void main(String[] args) {
        Scanner sc=new Scanner(System.in);
        int n=sc.nextInt();
        int[] p=new int[n+1];
        int[] res=new int[n+1];
        for(int i=1;i<=n;i++)
        {
            p[i]=sc.nextInt();
            res[p[i]]=i;
        }
        sc.close();
        for(int i=1;i<=n;i++)
        {
            System.out.print(res[i]+" ");
        }
    }

}