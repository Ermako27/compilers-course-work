mas = [1,2,3]
j = 10
counter = 0


def foo
    while j>=0 && mas[j] > mas[j+step]
        buf = mas[j]
        mas[j] = mas[j+step]
        mas[j+step] = buf
        j-=1
        for (i = 0; i < 10; i++)
            counter = counter + 1
        end
    end
end