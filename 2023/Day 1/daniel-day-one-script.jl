# Daniel day 1

# Solution plan

# Set a container
#Read input line by line, treat each character as an element
# Test whether the element is a decimal or digit 
# parse each element string character as number, index to find location and value of beginning number
# parse each element string character as number, index to find location and value of end number
# push these together
# add the collection of pushed number

input = readlines("inputs/day_1_dr.txt")

#Part1
function part1(data)
    cont = [] # Set a container
    for i in data  # for each element in the date input
        i = filter(isdigit, i) # test whether the character is a decimal digit
        n1 = parse(Int, string(i[begin])) # Parse string as number, indexing to find the location of the beginning number
        n2 = parse(Int, string(i[end])) # Parse string as number, indexing to find the location of the last number
        push!(cont, n1 * 10 + n2) # use the containter 
    end
    return sum(cont)
end

#Part2
# Create a dictionary
# Look at the specification of the problem, translate for the base using 1:9
# Use => to create pairs for the table
some_numbers = Dict("one" => "one1one", "two" => "two2two", "three" => 
"three3three", "four" => "four4four", "five" => "five5five", 
"six" => "six6six", "seven" => "seven7seven", "eight" => "eight8eight",
 "nine" => "nine9nine")

function cleaning(data, some_numbers) # some_numbers 
    for i in 1: length(data) 
        for key in keys(some_numbers) 
            data[i] = replace(data[i], key => some_numbers[key]) # resolve the paired numbers using dictionary above
        end
    end
    return data 
end 
part1(input)

input2 = cleaning(input, some_numbers) # now pass it back to input

 part1(input2)
