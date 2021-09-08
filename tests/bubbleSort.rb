def bubbleSort(a)
    size = 10
    for(i = 0; i<size; i+=1)
        for(j = size-1; j>i; j-=1)
            if(a[j-1] > a[j])
                x=a[j-1]
                a[j-1]=a[j]
                a[j]=x
            end
        end
    end
    return a
end

array = []
array[0] = 10
array[1] = 9
array[2] = 8

bubbleSort(array)