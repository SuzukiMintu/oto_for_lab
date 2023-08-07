import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


### エクスプローラーを開くための関数
def open_explorer():
    path = filedialog.askdirectory()
    path_entry.delete(0, tk.END)
    path_entry.insert(tk.END, path)

### oto.ini 生成用関数
def generate_oto_ini():
    
    ### テキストボックスに入力された情報を取得
    path = path_entry.get()
    prolong = prolong_entry.get()
    suffix = suffix_entry.get()

    if not path:
        messagebox.showerror("エラー", "パスの指定がされていません。")
        return

    if not prolong:
        messagebox.showerror("エラー", "伸ばしの数が指定されていません。")
        return

    if not prolong.isdigit():
        messagebox.showerror("エラー", "伸ばしの数は半角数字で入力してください。")
        return

    else:
        prolong = int(prolong)

    ### 指定されたパスの中にあるファイル名の取得
    try:
        sounds_list = os.listdir(path)
    except:
        messagebox.showerror("エラー", f"ファイル名の取得に失敗しました。\n\n指定されたパスが存在しない可能性があります。指定したパスをご確認ください。\n\n指定されたパス：\"{path}\"")
        return

    ### 指定されたパスの中に oto.ini を作成。もし oto.ini が元から存在していた場合はバックアップを作成する
    for i in range(len(sounds_list)):
        if "oto.ini" == sounds_list[i]:
            if messagebox.askyesno("確認", "既に存在する oto.ini を見つけました。\nバックアップを作成して操作を続行しますか？"):
                shutil.copyfile(rf"{path}\\oto.ini", rf"{path}\\oto_backup.ini")
                break
            else:
                return

    ### oto.ini を初期化する
    try:
        with open(f"{path}\\oto.ini", "w", encoding="Shift_JIS") as otoini:
            otoini.write("")
    except:
        messagebox.showerror("エラー", f"oto.ini の新規作成に失敗しました。指定したパスのアクセス権限をご確認ください。\n\n指定されたパス：\"{path}\"")
        return

    ### 読み込んだlabファイルの数確認用
    sounds_quantity = 0

    ### 生成したエイリアスを保存する用の配列変数
    alias_memory = []

    ### 取得したファイル名からlabファイルだけを抽出して読み込む
    for i in sounds_list:
        if i.endswith(".lab"):
            sounds_quantity += 1
            lab_filename_old = i.replace(".lab", "")
            lab_filename = lab_filename_old.replace("0", "").replace("1", "").replace("2", "").replace("3", "").replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace("8", "").replace("9", "").replace("ー", "").replace("...", "").replace(" ", "").replace("-", "")
            if not lab_filename_old.startswith("_"):
                lab_filename = "_" + lab_filename
            lab_filename_list = []

            ### ファイル名に連番や伸ばし棒、VOICEVOXの文字省略されたときの三点やその他不要な文字がある場合、またファイル名の最初にアンダーバーが無い場合は名前変更をする
            if lab_filename_old.endswith("0") or lab_filename_old.endswith("1") or lab_filename_old.endswith("2") or lab_filename_old.endswith("3") or lab_filename_old.endswith("4") or lab_filename_old.endswith("5") or lab_filename_old.endswith("6") or lab_filename_old.endswith("7") or lab_filename_old.endswith("8") or lab_filename_old.endswith("9") or "ー" in lab_filename_old or "..." in lab_filename_old or " " in lab_filename_old or "-" in lab_filename_old:
                try:
                    os.rename(f"{path}\\{lab_filename_old}.lab", f"{path}\\{lab_filename}.lab")
                except:
                    messagebox.showerror("エラー", f"ファイル名の変更に失敗しました。同じ名前のlabファイル(連番などは除く)が存在する可能性があります。\n\n失敗したファイル名：{lab_filename_old}.lab")
                    os.remove(f"{path}\\oto.ini")
                    return
                try:
                    os.rename(f"{path}\\{lab_filename_old}.wav", f"{path}\\{lab_filename}.wav")
                except:
                    messagebox.showerror("エラー", f"ファイル名の変更に失敗しました。labファイルと同名のwavファイルが存在することをご確認ください。\n\n失敗したファイル名：{lab_filename_old}.wav")
                    os.rename(f"{path}\\{lab_filename}.lab", f"{path}\\{lab_filename_old}.lab")
                    os.remove(f"{path}\\oto.ini")
                    return
        
            ### ファイル名のリスト化
            for lab_filename_i in range(len(list(lab_filename))):
                if "ぁ" == list(lab_filename)[lab_filename_i] or "ぃ" == list(lab_filename)[lab_filename_i] or "ぅ" == list(lab_filename)[lab_filename_i] or "ぇ" == list(lab_filename)[lab_filename_i] or "ぉ" == list(lab_filename)[lab_filename_i] or "ゃ" == list(lab_filename)[lab_filename_i] or "ゅ" == list(lab_filename)[lab_filename_i] or "ょ" == list(lab_filename)[lab_filename_i]:
                    lab_filename_list[len(list(lab_filename_list)) - 1] += str(list(lab_filename)[lab_filename_i])
                else:
                    lab_filename_list.append(list(lab_filename)[lab_filename_i])

            ### labファイルの名前からlabファイルの中身を取得
            try:
                with open(f"{path}\\{lab_filename}.lab", "r", encoding="UTF-8") as lab_file:
                    lab_data = lab_file.read().replace("N", "n").splitlines()
            except:
                messagebox.showerror("エラー", f"labファイルの読み込みに失敗しました。\n\n失敗したファイル名：{lab_filename_old}.lab")
                return

            ### 取得したlabファイルの中身の一行目に無音用の行がある場合は削除
            if lab_data[0].endswith("pau") or lab_data[0].endswith("sil"):
                del lab_data[0]

            ### labファイルから oto.ini の中身を生成   ※oto.ini に書き込むときはパラメータが左から、エイリアス・左ブランク・固定範囲・右ブランク・先行発声・オーバーラップの順になるようにする
            lab_data_prolong = 0

            try:
                for lab_filename_i in range(len(lab_filename_list)):

                    ### 一文字目が"_"の場合で尚且つ未生成のエイリアスの場合は単独音エイリアスを生成する
                    if "_" == lab_filename_list[lab_filename_i] and not lab_filename_list[lab_filename_i + 1] in alias_memory:
                
                        ### labファイル名とlabファイルの中身からwavファイルの指定とエイリアスと左ブランクとオーバーラップを設定。同時に生成したエイリアスを保存する
                        left_blank = int(lab_data[0].split()[0]) / 10000
                        overlap = int(lab_data[0].split()[1]) / 10000 - left_blank
                        alias_memory.append(f"{lab_filename_list[lab_filename_i + 1]}")

                        ### labファイルの中にある音素情報から子音音素の行だけを検知して、同時に先行発声を設定
                        if lab_data[0].split()[2] == lab_data[1].split()[2]:
                            preutterance = int(lab_data[0].split()[0]) / 10000 - left_blank
                            lab_data_prolong += prolong
                            
                        elif lab_data[1].split()[2] == lab_data[2].split()[2]:
                            preutterance = int(lab_data[1].split()[0]) / 10000 - left_blank
                            lab_data_prolong += prolong + 1
                    
                        else:
                            preutterance = int(lab_data[1].split()[0]) / 10000 - left_blank
                            lab_data_prolong += prolong + 2
                
                        ### 固定範囲と右ブランクの設定
                        consonant = int(lab_data[lab_data_prolong - prolong + 1].split()[1]) / 10000 - left_blank
                        right_blank = int(lab_data[lab_data_prolong - 2].split()[0]) / 10000 - left_blank

                        ### 最後に全パラメータを順番に追記
                        with open(f"{path}\\oto.ini", "a", encoding="Shift_JIS") as otoini:
                            otoini.write(f"{lab_filename}.wav={lab_filename_list[lab_filename_i + 1]}{suffix},{left_blank},{consonant},-{right_blank},{preutterance},{overlap}\n")

                        ### 連続音エイリアス生成時に lab_data_prolong が 0 でないとバグるため値をリセットする
                        lab_data_prolong = 0

                    ### 一文字目が"_"でない場合で尚且つ未生成のエイリアスの場合は連続音エイリアスを生成する
                    elif not "_" == lab_filename_list[lab_filename_i] and not (("_" == lab_filename_list[lab_filename_i - 1] and f"- {lab_filename_list[lab_filename_i]}" in alias_memory) or (not "_" == lab_filename_list[lab_filename_i - 1] and f"{lab_data[lab_data_prolong - 1].split()[2]} {lab_filename_list[lab_filename_i]}" in alias_memory)):

                        ### labファイル名とlabファイルの中身からwavファイルの指定とエイリアスと左ブランクとオーバーラップを設定。同時に生成したエイリアスを保存する
                        with open(f"{path}\\oto.ini", "a", encoding="Shift_JIS") as otoini:
                            otoini.write(f"{lab_filename}.wav=")
                            if "_" == lab_filename_list[lab_filename_i - 1]:
                                left_blank = int(lab_data[lab_data_prolong].split()[0]) / 10000
                                overlap = 0.0
                                otoini.write(f"- {lab_filename_list[lab_filename_i]}{suffix},{left_blank},")
                                alias_memory.append(f"- {lab_filename_list[lab_filename_i]}")
                            else:
                                left_blank = int(lab_data[lab_data_prolong - 2].split()[0]) / 10000
                                overlap = int(lab_data[lab_data_prolong - 2].split()[1]) / 10000 - left_blank
                                otoini.write(f"{lab_data[lab_data_prolong - 1].split()[2]} {lab_filename_list[lab_filename_i]}{suffix},{left_blank},")
                                alias_memory.append(f"{lab_data[lab_data_prolong - 1].split()[2]} {lab_filename_list[lab_filename_i]}")

                        ### labファイルの中にある音素情報から子音音素の行だけを検知して、同時に先行発声を設定
                        if lab_data[lab_data_prolong].split()[2] == lab_data[lab_data_prolong + 1].split()[2]:
                            preutterance = int(lab_data[lab_data_prolong].split()[0]) / 10000 - left_blank
                            lab_data_prolong += prolong
                            
                        elif lab_data[lab_data_prolong + 1].split()[2] == lab_data[lab_data_prolong + 2].split()[2]:
                            preutterance = int(lab_data[lab_data_prolong + 1].split()[0]) / 10000 - left_blank
                            lab_data_prolong += prolong + 1
                    
                        else:
                            preutterance = int(lab_data[lab_data_prolong + 1].split()[0]) / 10000 - left_blank
                            lab_data_prolong += prolong + 2

                        ### 固定範囲と右ブランクの設定
                        consonant = int(lab_data[lab_data_prolong - prolong + 1].split()[1]) / 10000 - left_blank
                        right_blank = int(lab_data[lab_data_prolong - 2].split()[0]) / 10000 - left_blank
                
                        ### 最後に左ブランクとエイリアス以外のパラメータを順番に追記
                        with open(f"{path}\\oto.ini", "a", encoding="Shift_JIS") as otoini:
                            otoini.write(f"{consonant},-{right_blank},{preutterance},{overlap}\n")
                
                    ### 連続音エイリアスもVCエイリアスも既に生成済みだった場合、lab_data_prolong の値だけ変えておく
                    elif not "_" == lab_filename_list[lab_filename_i] and (("_" == lab_filename_list[lab_filename_i - 1] and f"- {lab_filename_list[lab_filename_i]}" in alias_memory) or (not "_" == lab_filename_list[lab_filename_i - 1] and f"{lab_data[lab_data_prolong - 1].split()[2]} {lab_filename_list[lab_filename_i]}" in alias_memory)):
                        if lab_data[lab_data_prolong].split()[2] == lab_data[lab_data_prolong + 1].split()[2]:
                            lab_data_prolong += prolong
                            
                        elif lab_data[lab_data_prolong + 1].split()[2] == lab_data[lab_data_prolong + 2].split()[2]:
                            lab_data_prolong += prolong + 1
                    
                        else:
                            lab_data_prolong += prolong + 2

                    ### 一文字目が"_"でない&次の発音が母音じゃない&現在位置が最後の発音じゃない場合で尚且つ未生成のエイリアスの場合はVCエイリアスを生成する
                    if not "_" == lab_filename_list[lab_filename_i] and 1 < len(lab_filename_list) - lab_filename_i and not (lab_filename_list[lab_filename_i + 1].startswith("あ") or lab_filename_list[lab_filename_i + 1].startswith("い") or lab_filename_list[lab_filename_i + 1].startswith("う") or lab_filename_list[lab_filename_i + 1].startswith("え") or lab_filename_list[lab_filename_i + 1].startswith("お") or lab_filename_list[lab_filename_i + 1].startswith("ん")) and not f"{lab_data[lab_data_prolong - 1].split()[2]} {lab_data[lab_data_prolong].split()[2]}" in alias_memory:

                        ### labファイル名とlabファイルの中身から全パラメータを設定。同時に生成したエイリアスを保存する
                        left_blank = int(lab_data[lab_data_prolong - 2].split()[0]) / 10000
                        consonant = int(lab_data[lab_data_prolong].split()[0]) / 10000 - left_blank
                        right_blank = int(lab_data[lab_data_prolong].split()[1]) / 10000 - left_blank
                        preutterance = int(lab_data[lab_data_prolong].split()[0]) / 10000 - left_blank
                        overlap = int(lab_data[lab_data_prolong - 2].split()[1]) / 10000 - left_blank
                        alias_memory.append(f"{lab_data[lab_data_prolong - 1].split()[2]} {lab_data[lab_data_prolong].split()[2]}")
                        with open(f"{path}\\oto.ini", "a", encoding="Shift_JIS") as otoini:
                            otoini.write(f"{lab_filename}.wav={lab_data[lab_data_prolong - 1].split()[2]} {lab_data[lab_data_prolong].split()[2]}{suffix},{left_blank},{consonant},-{right_blank},{preutterance},{overlap}\n")

                    ### 現在位置が最後の発音だった場合は語尾音エイリアスを作成する
                    elif 1 == len(lab_filename_list) - lab_filename_i and not f"{lab_data[lab_data_prolong - 1].split()[2]} R" in alias_memory:

                        ### labファイル名とlabファイルの中身から全パラメータを設定。同時に生成したエイリアスを保存する
                        left_blank = int(lab_data[lab_data_prolong - 2].split()[0]) / 10000
                        consonant = int(lab_data[lab_data_prolong - 1].split()[1]) / 10000 - left_blank + 100
                        right_blank = int(lab_data[lab_data_prolong - 1].split()[1]) / 10000 - left_blank + 200
                        preutterance = int(lab_data[lab_data_prolong - 1].split()[1]) / 10000 - left_blank
                        overlap = int(lab_data[lab_data_prolong - 2].split()[1]) / 10000 - left_blank
                        alias_memory.append(f"{lab_data[lab_data_prolong - 1].split()[2]} R")
                        with open(f"{path}\\oto.ini", "a", encoding="Shift_JIS") as otoini:
                            otoini.write(f"{lab_filename}.wav={lab_data[lab_data_prolong - 1].split()[2]} R{suffix},{left_blank},{consonant},-{right_blank},{preutterance},{overlap}\n")
            except:
                messagebox.showerror("エラー", f"パラメータの生成中にエラーが発生しました。labファイルのデータが正常でないか、または伸ばしの数の値が間違っている可能性があります。\n\n失敗したファイル名：{lab_filename_old}.lab\n\n生成に失敗した oto.ini を oto_error.ini として保存します。")
                shutil.copyfile(rf"{path}\\oto.ini", rf"{path}\\oto_error.ini")
                os.remove(f"{path}\\oto.ini")
                return

    if 0 == sounds_quantity:
        messagebox.showerror("エラー", f"labファイルが見つかりませんでした。指定したパスの中にlabファイルがあることをご確認ください。\n\n指定されたパス：\"{path}\"")
        os.remove(f"{path}\\oto.ini")
        return
    
    ### 読み込んだlabファイルの数確認用
    messagebox.showinfo("成功", f"oto.iniを生成しました。\n読み込んだlabファイル数：{sounds_quantity}")



### UIを作成
root = tk.Tk()
root.title("oto for lab - ver 1.0.0")
root.geometry("800x450")

root.resizable(True, False)
root.minsize(width=800, height=450)

title_label = tk.Label(root, text="oto for lab", font=("Helvetica", 40))
title_label.pack()

version_label = tk.Label(root, text="ver 1.0.0\n", font=("Helvetica", 10), anchor="e")
version_label.pack(fill="x")

path_label = tk.Label(root, text="パスの指定：")
path_label.pack(anchor="w")

### パスの指定のテキストボックスに初期値を設定
path_entry = tk.Entry(root)
path_entry.insert(tk.END, "C:")
path_entry.pack(fill="x")

### エクスプローラーを開くボタンを追加
explorer_button = tk.Button(root, text="エクスプローラーを開いてパスを指定", command=open_explorer)
explorer_button.pack(anchor="w")

path_description_label = tk.Label(root, text="絶対パスで指定する。例：C:\\Program Files (x86)\\UTAU\\voice\\uta\n")
path_description_label.pack(anchor="w")

prolong_label = tk.Label(root, text="伸ばしの数：")
prolong_label.pack(anchor="w")

### 伸ばしの数のテキストボックスに初期値を設定
prolong_entry = tk.Entry(root)
prolong_entry.insert(tk.END, "6")
prolong_entry.pack(fill="x")

prolong_description_label = tk.Label(root, text="発音の際に使った伸ばし棒の数+1。A.I.VOICEのフレーズ内で｢アーーーーー｣と伸ばした場合、伸ばし棒は5個なのでこれに+1で 6 に設定。\n")
prolong_description_label.pack(anchor="w")

suffix_label = tk.Label(root, text="表情エイリアス：")
suffix_label.pack(anchor="w")

suffix_entry = tk.Entry(root)
suffix_entry.pack(fill="x")

path_description_label = tk.Label(root, text="UTAU音源でよく見る｢↑｣とかのアレ。特に無ければ指定無しでOK。\n")
path_description_label.pack(anchor="w")

generate_button = tk.Button(root, text="oto.ini 生成", font=("Helvetica", 20), command=generate_oto_ini)
generate_button.pack(side=tk.BOTTOM)



root.mainloop()

