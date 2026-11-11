def max_rect_in_rect_advanced(A_w, A_h, B_w, B_h):
    # Если размеры некорректны или B больше A в обеих ориентациях
    if A_w <= 0 or A_h <= 0 or B_w <= 0 or B_h <= 0:
        return 0
        
    def solve(aw, ah, bw, bh):
        if aw < bw or ah < bh:
            return 0
            
        # Сколько целых рядов и колонок помещается
        cols = aw // bw
        rows = ah // bh
        current_fit = cols * rows
        
        # Остатки по ширине и высоте
        rem_w = aw - (cols * bw)
        rem_h = ah - (rows * bh)
        
        # Рекурсивно проверяем укладку повернутых фигур B(bh x bw) в оставшиеся зоны:
        # Вариант А: Поворачиваем в остатке по ширине (справа) + остаток снизу
        option_a = current_fit + solve(rem_w, ah, bh, bw) + solve(cols * bw, rem_h, bh, bw)
        
        # Вариант Б: Поворачиваем в остатке по высоте (снизу) + остаток справа
        option_b = current_fit + solve(aw, rem_h, bh, bw) + solve(rem_w, rows * bh, bh, bw)
        
        return max(option_a, option_b)

    # Проверяем два базовых размещения (начинаем укладку B как есть, либо сразу повернув B)
    variant_1 = solve(A_w, A_h, B_w, B_h)
    variant_2 = solve(A_w, A_h, B_h, B_w)
    
    return max(variant_1, variant_2)

def main():
    print("--- Оптимизированный расчет укладки фигур ---")
    try:
        a_w = float(input("Ширина фигуры A: "))
        a_h = float(input("Высота фигуры A: "))
        b_w = float(input("Ширина фигуры B: "))
        b_h = float(input("Высота фигуры B: "))
        
        # Валидация данных
        if any(x <= 0 for x in [a_w, a_h, b_w, b_h]):
            print("**Ошибка: Все размеры должны быть больше нуля!**")
            return
            
        result = int(max_rect_in_rect_advanced(a_w, a_h, b_w, b_h))
        print(f"\n**Максимальное количество фигур B в фигуре A: {result}**")
        
    except ValueError:
        print("**Ошибка ввода: Пожалуйста, вводите только числовые значения.**")

if __name__ == "__main__":
    main()
