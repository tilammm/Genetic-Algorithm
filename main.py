from PIL import Image, ImageDraw,ImageChops
import numpy
import random
import math


def empty_image(image):
    for i in range(len(image)):
        for j in range(len(image[0])):
            image[i][j][0] = 255
            image[i][j][1] = 255
            image[i][j][2] = 255
    return image


def cal_fitness(image, input_image):
    diff = ImageChops.difference(image, input_image)
    h = diff.histogram()
    sq = (value * (idx ** 2) for idx, value in enumerate(h))
    sum_of_squares = sum(sq)
    fitness = math.sqrt(sum_of_squares / float(image.size[0] * image.size[1]))
    return 1/fitness


def sort_by_fitness(population, fitness):
    array = (zip(fitness, population))
    fitness, population = zip(*sorted(array, key=lambda x: x[0]))
    return fitness, population


def get_paresnts(population):
    result = []
    if len(population) == 2:
        result.append(population[0])
        result.append(population[1])
    else:
        for i in range(2):
            index = (len(population) - i - 1)
            result.append(population[index])
    return result


def crossover(parents):
    result = []
    parent1 = numpy.asarray(parents[0])
    parent2 = numpy.asarray(parents[1])
    child1 = parent1.copy()
    child2 = parent2.copy()
    for k in range(random.randint(1, 5)):
        x0 = random.randint(0, 512)
        y0 = random.randint(0, 512)
        x1 = random.randint(x0, 512)
        y1 = random.randint(y0, 512)
        for i in range(x1 - x0):
            for j in range(y1-y0):
                child1[x0 + i][y0 + j] = parent2[x0 + i][y0 + j]

    for k in range(random.randint(1, 5)):
        x0 = random.randint(0, 512)
        y0 = random.randint(0, 512)
        x1 = random.randint(x0, 512)
        y1 = random.randint(y0, 512)
        for i in range(x1 - x0):
            for j in range(y1-y0):
                child2[x0 + i][y0 + j] = parent1[x0 + i][y0 + j]

    result.append(Image.fromarray(child1))
    result.append(Image.fromarray(child2))

    return result


def mutation(image):
    copy_of_image = image.copy()
    redactor = ImageDraw.Draw(copy_of_image)
    if random.randint(1, 2) == 1:
        for i in range(random.randint(1, 30)):
            x0 = random.randint(0, 312)
            y0 = random.randint(0, 312)
            x1 = random.randint(x0, x0+200)
            y1 = random.randint(y0, y0+200)
            red = random.randint(1, 244)
            green = random.randint(1, 244)
            blue = random.randint(1, 244)
            start = random.randint(3, 12)
            end = random.randint(0, 6)
            redactor.arc([(x0, y0), (x1, y1)], start=start, end=end, fill=(red, green, blue))
    else:
        for i in range(random.randint(1, 30)):
            x0 = random.randint(0, 462)
            y0 = random.randint(0, 462)
            x1 = random.randint(x0, x0+50)
            y1 = random.randint(y0, y0+50)
            red, green, blue = image.getpixel((x0, y0))
            green = random.randint(1, 244)
            blue = random.randint(1, 244)
            start = random.randint(3, 12)
            end = random.randint(0, 6)
            redactor.arc([(x0, y0), (x1, y1)], start=start, end=end, fill=(red, green, blue))
    result = Image.blend(image, copy_of_image, 0.6)
    return result


image_list = []
path = str(input('Enter name of image: '))
input_image = Image.open(path)
input_image = input_image.convert('RGB')
first_parent = Image.new('RGB', (512, 512), (256, 256, 256))
second_parent = Image.new('RGB', (512, 512), (256, 256, 256))

image_list.append(first_parent)
image_list.append(second_parent)

number_of_generation = int(input('Number of generation(30,000 recommended): '))
generation = 0
while generation < number_of_generation:
    fitness = []
    for image in image_list:
        fit = cal_fitness(image, input_image)
        fitness.append(fit)
    fitness, image_list = sort_by_fitness(image_list, fitness)
    parents = get_paresnts(image_list)
    if generation % 500 == 0:
        print('-------End of generation #', generation, '-------')
    new_generation = crossover(parents)
    image_list = []
    image_list = parents + new_generation
    for index in range(len(image_list)):
        image_list.append(mutation(image_list[index]))
    generation += 1

total_fitness = []
for image in image_list:
    fit = cal_fitness(image, input_image)
    total_fitness.append(fit)
total_fitness, image_list = sort_by_fitness(image_list, total_fitness)
result = image_list[len(image_list) - 1]
result.save('result.png')


