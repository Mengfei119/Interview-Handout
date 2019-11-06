package workshop;

public class Price {
	static int solution(int arr[]) {
		if (arr == null || arr.length < 3)
			return 0;
		int n= arr.length;
		int res= 0;
		for (int j= 1; j < n - 1; j++ ) {
			int right= 0;
			for (int k= j + 1; k < n; k++ )
				if (arr[j] > arr[k])
					right++ ;

			// count all greater elements on left of arr[i]
			int left= 0;
			for (int i= j - 1; i >= 0; i-- )
				if (arr[i] > arr[j])
					left++ ;

			res+= left * right;
		}
		return res;
	}

	public static void main(String args[]) {
		int arr[]= new int[] { 9, 6, 4, 5, 8 };
		System.out.print(solution(arr));
	}

}
