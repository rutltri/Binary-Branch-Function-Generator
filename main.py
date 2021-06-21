import math
import tkinter as tk
from tkinter import messagebox
import pathlib
from pathlib import Path as path
import os
from tkinter.constants import TRUE

class system:
    def gen(self):
        def folder_gen(self):
            def path_gen(self,i,digit,post,post_s):
                #Path generate. l = ["(PreNumbers)","(4 InsideNumbers)",...] | postnum = "(3 PostNumbers)"
                _ = bin(i)[2:].zfill(digit)
                postnum = _[-post_s:]
                __ = _[:-post]
                if not len(__)%4 == 0:
                    #Put the number of remainder digits at the PreNumber.
                    ___ = (len(__)%4)
                    l = [__[:___]]
                    __ = __[___:]
                else:
                    l =[]
                while len(__) > 0:
                    #Add InsideNumber to l.
                    l.append(__[:4])
                    __ = __[4:]
                return l,postnum

            def path_sum(self,i,Inside,digit,l_digit,p:bool):
                l = []
                if l_digit > 0:
                    _ = bin(Inside)[2:].zfill(l_digit)
                    if not len(_)%4 == 0:
                        ___ = (len(_)%4)
                        l.append(_[:___])
                        _ = _[___:]
                    while len(_) > 0:
                        l.append(_[:4])
                        _ = _[4:]

                if p == False:
                    postnum = bin(i)[2:].zfill(digit)
                elif p == True:
                    postnum = ""
                return l,postnum

            def path_output(_,__,___,max_digit):
                printpath = path(self.folder) / "branch" / "/".join(_) / (__+"p.mcfunction")
                print(_,printpath)
                branch_func = ""
                if __ == "":
                    pass
                elif type(__) is str:
                    __ = int(__,2)
                    branch_func = (bin(__)[2:].zfill(___))
                branch_point(self,_,branch_func,max_digit)
                return printpath

            dirbranch = path(self.folder) / "branch"
            dirbranch.mkdir(parents=True)

            if self.branch_count > 1:
                #Lowest branch generate.
                for i in range(self.branch_count):
                    l, postnum = path_gen(self,i,math.ceil(math.log2(self.branch_count)),3,3)
                    upper_output = path(self.folder) / "branch" / "/".join(l) / (postnum+"p.mcfunction")
                    print(i,upper_output)
                    print(l,postnum)
                    if upper_output.parent.exists() == False:
                        upper_output.parent.mkdir(parents=True)
                    upper_output.write_text(output_gen(self,i))
            else:
                postnum = ""

            postnum = postnum[:-1]
            _l = []
            try:
                l
            except:
                pass
            else:
                _l += l
            if not postnum == "":
                _l.append(postnum)

            #Gen Branch mcfunction
            if not len(_l) == 0:
                bot_digit = 1
                while len(_l) > 0:
                    #There are two or more elements in the list.
                    try:
                        _l[-2]
                    except:
                        ___c = 0
                        l_digit = 0
                    else:
                        ___c = int("".join(_l[:-1]),2)
                        l_digit = math.floor(math.log2(___c))+1

                    #Loop by the number of elements of _l. ["nnnn","nnnn","nnnn"] = 2
                    while ___c >= 0:

                        try:
                            _l[-1]
                        except:
                            _c = 0
                            digit = 0
                        else:
                            _c = max(1,int(_l[-1],2))
                            digit = math.floor(math.log2(_c))+1
                            max_digit = digit + bot_digit

                        #Loop by the number of postnumber.
                        while digit > 0:
                            __c = _c
                            while __c >= 0:
                                print("keta",digit,bot_digit)
                                _, __ = path_sum(self,__c,___c,digit,l_digit,False)
                                path_output(_,__,digit,max_digit)
                                __c -= 1
                            else:
                                digit -= 1
                                _c //= 2
                        _,__ = path_sum(self,__c,___c,digit,l_digit,True)
                        path_output(_,__,digit,max_digit)
                        ___c -= 1
                    _l.pop()
                    bot_digit = 0

                    #Distinguish of undefined and blank
                    try:
                        _l[-1]
                    except:
                        pass
                    else:
                        _l[-1] = _l[-1][:-1]
                        if _l[-1] == "":
                            _l.pop()
                        path_output("","",0,_c)

            else:
                path_output("","",0,0)

                #Generate a branch function.
                #Remove the bottom path.
                #See the upper path.

        def branch_point(self,l,branch_func,max_digit):
            #Generate a pointer function between folders.
            branch_path = path(self.folder) / "branch" / "/".join(l) / (branch_func +"p"+".mcfunction")
            branch_path.write_text(pointer_gen(self,l,branch_func,max_digit))
            #print(pointer_gen(self,l,branch_func))

        def output_gen(self,i):
            c = i
            c = (c+1)*2-1
            run = "function "+self.funcId.get()+self.folder
            _ = "execute unless "+eval(self.syntax_init())
            __ = "execute if "+eval(self.syntax_init())
            return _+run+"/outputs/"+str(i*2)+"\n"+__+run+"/outputs/"+str(i*2+1)

        def pointer_gen(self,l,branch_func,max_digit):
            if max_digit > len(branch_func) and not l == "":
                zbp = branch_func+"0"+"p"
                xbp = branch_func+"1"+"p"
            else:
                zbp = branch_func+"0"+"/p"
                xbp = branch_func+"1"+"/p"
            score = self.branch_count

            add_s = score//2

            for i in "".join(l)+branch_func:
                if i == "0":
                    score -= add_s
                elif i == "1":
                    score += add_s
                add_s //= 2
            # c is converted with syntax_init
            c = score
            if l:
                _l = "/".join(l)+"/"
            else:
                _l = ""
            run = "function "+self.funcId.get()+self.folder+"/branch/"+_l
            _ = "execute unless "+eval(self.syntax_init())
            __ = "execute if "+eval(self.syntax_init())
            return _+run+zbp+"\n"+__+run+xbp

        self.var = self.score.get()
        self.count = int(self.comp.get())
        self.folder = self.title.get()

        if os.path.isdir(self.folder):
            messagebox.showerror("FolderExistsError","指定したフォルダが既に存在しています。")
        elif not 0 < len(self.folder):
            messagebox.showerror("FolderNameEmptyError","フォルダ名を指定してください。")
        elif not 1 < self.count < 4097:
            messagebox.showerror("ComponentOutOfRangeError","範囲内の値を指定してください。")
        else:
            self.branch_count = -(-self.count-1)//2
            folder_gen(self)

            output = path(self.folder+"/outputs")
            output.mkdir(parents=True)

            for c in range(self.count):
                output_func = (output / str(c)).with_suffix(".mcfunction")
                output_func.write_text(self.return_command(c))

            messagebox.showinfo("GenerationCompleted","生成が完了しました。")


    def return_command(self,c):
        def return_count(self,syntax,c):
            # Return component count. String Storage list for True, String int for False.
            if syntax == True:
                i = bin(c)[2:].zfill(len(bin(int(self.comp.get())-1)[2:]))
                l = ""
                for u in i:
                    l = l + "["+u+"]"
                return l
            else:
                return str(c)
        # Translate Run Command
        run = self.run.get(1.0,"end-1c")
        run = run.replace("$~i",return_count(self,False,c))
        run = run.replace("$~bi",return_count(self,True,c))
        return run

    def syntax_init(self):
        # Command syntax conversion
        if self.command_syn.get() == "0":
            return "(\"entity \"+self.target.get()+\"[scores={\"+self.score.get()+\"=\"+str (c)+\"..}] run \")"
        else:
            return "(\"score \"+self.target.get()+\" \"+self.score.get()+\" matches \"+str  (c)+\".. run \")"

    def view_gen(self):
        c = 1
        view_run = self.return_command(c)
        self.run_view["text"] = ("if "+eval(self.syntax_init())+view_run)

    def path_clone(self, var, indx, mode):
        self.funcIdP.delete(0,tk.END)
        if str(self.funcId.get())[-1] == ":":
            self.funcIdP.insert(tk.END,self.title.get())
        else:
            self.funcIdP.insert(tk.END,"/"+self.title.get())
        return True

    def comp_between(self, var, indx, mode):

        try:
            _ = max(2,min(4096,int(self.comp.get())))
        except:
            self.comp.delete(0,tk.END)
            return False
        else:
            self.comp.delete(0,tk.END)
            self.comp.insert(tk.END,_)
            return True

    def __init__(self):
        self.command_syn = tk.StringVar()
        self.func_path = tk.StringVar()
        self.comp_max = tk.StringVar()
        #self.comp = 0

        self.command_syn.set("0")
        self.button = tk.Button(text="Generate",command=self.gen)
        self.button.place(width=100,relx=0.2,rely=0.8)
        self.titleL = tk.Label(text="Folder Name")
        self.titleL.place(x=20,y=30)
        self.title = tk.Entry(textvariable=self.func_path)
        self.title.insert(tk.END,"binary")
        self.title.place(width=380,x=180,y=30)

        self.compL = tk.Label(text="Component Count(1~4096)")
        self.compL.place(x=20,y=60)
        self.comp = tk.Spinbox(from_=2,to_=4096,validate="all",textvariable=self.comp_max)
        self.comp.place(x=180,y=60)

        self.scoreL = tk.Label(text="Score Name")
        self.scoreL.place(x=20,y=90)
        self.score = tk.Entry()
        self.score.insert(tk.END,"var")
        self.score.place(x=180,y=90)

        self.targetL = tk.Label(text="Target Name")
        self.targetL.place(x=20,y=180)
        self.target = tk.Entry()
        self.target.insert(tk.END,"@s")
        self.target.place(x=180,y=180)

        self.funcIdL = tk.Label(text="Function Id")
        self.funcIdL.place(x=20,y=120)
        self.funcId = tk.Entry()
        self.funcId.insert(tk.END,"namespace:")
        self.funcId.place(width=200,x=180,y=120)
        self.funcIdP = tk.Entry()
        self.funcIdP.insert(tk.END,"binary")
        self.funcIdP.place(width=160,x=400,y=120)

        self.command_syn1 = tk.Radiobutton(variable=self.command_syn,value="0",command=self.view_gen,text="entity")
        self.command_syn1.place(x=20,y=150)
        self.command_syn2 = tk.Radiobutton(variable=self.command_syn,value="1",command=self.view_gen,text="score")
        self.command_syn2.place(x=100,y=150)
        self.run_view = tk.Label(text="")
        self.run_view.place(x=180,y=150)

        self.runL = tk.Label(text="Run Command | Count=$~i, List=$~bi)")
        self.runL.place(x=20,y=210)
        self.run = tk.Text(height=5)
        self.run.insert(tk.END,"say \"This is $~i.\"")
        self.run.place(width=540,x=20,y=240)

        self.func_path.trace_add("write", self.path_clone)
        self.comp_max.trace_add("write",self.comp_between)
        self.view_gen()

main = tk.Tk()
main.geometry('600x400')
main.resizable(width=0,height=0)
main.title('Binary Branch Function Generator')

sys = system()

main.mainloop()