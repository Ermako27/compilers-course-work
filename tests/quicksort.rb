def quicksort(arr, first, last)
    if first < last
      p_index = partition(arr, first, last)
      quicksort(arr, first, p_index - 1)
      quicksort(arr, p_index + 1, last)
    end
  
    return arr
end
  
def partition(arr, first, last)
    pivot = arr[last]
    p_index = first
    
    def printer
        a = 'hello'
        b = 'world'
        return a
    end

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

    c = printer()
    temp = arr[p_index]
    arr[p_index] = pivot
    arr[last] = temp
    return p_index
end

unsorted = [5,6,3,1,8,4]
a = quicksort(unsorted,1,2)