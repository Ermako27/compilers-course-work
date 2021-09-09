def foo1(arg1)
    size = 10
    a = []
    for(i = 0; i<size; i+=1)
        for(j = size-1; j>i; j-=1)
            if(a[j-1] > a[j])
                x=a[j-1]
                a[j-1]=a[j]
                a[j]=x
            end
        end
    end
end

def foo2(arg1,arg2)
    first = 1
    i = first
    last = 10
    arr = []
    pivot =10
    p_index = 11
    while i < last
      if arr[i] <= pivot
        temp = arr[i]
        arr[i] = arr[p_index]
        arr[p_index] = temp
        p_index += 1
      end
      i += 1
    end
  
    foo1(i)
    foo1(i)
    foo2(i,2)
    temp = arr[p_index]
    arr[p_index] = pivot
    arr[last] = temp
end

def foo3(arg1,arg2,arg3)
    first = 1
    i = first
    last = 10
    arr = []
    pivot =10
    p_index = 10
    while i < last
      if arr[i] <= pivot
        temp = arr[i]
        arr[i] = arr[p_index]
        arr[p_index] = temp
        p_index += 1
      end
      i += 1
    end
  
    foo2(1,2)
    foo3(first,1 ,2)
    temp = arr[p_index]
    arr[p_index] = pivot
    arr[last] = temp
end

def partition(arr, first, last)
    pivot = arr[last]
    p_index = first
    
    def printer
        a = 'hello'
        b = 'world'
        return a
    end
    arr= []
    i = first
    while i < last
      if arr[i] <= pivot
        temp = arr[i]
        arr[i] = arr[p_index]
        arr[p_index] = temp
        p_index += 1
      end
      i += 1
    end
    foo3(p_index, first, last)
    c = printer()
    temp = arr[p_index]
    arr[p_index] = pivot
    arr[last] = temp
    return p_index
end
  
  
def quicksort(arr, first, last)
    if first < last
      p_index = partition(arr, first, last)
      quicksort(arr, first, p_index - 1)
      quicksort(arr, p_index + 1, last)
    end
    
    return arr
end
  
unsorted = [5,6,3,1,8,4]
a = quicksort(unsorted,1,2);