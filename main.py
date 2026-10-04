import re, collections, tkinter as tk
from pathlib import Path
from tkinter import filedialog,messagebox
BG='#09121F';CARD='#142039';TEXT='#F5F8FF';MUTED='#B0BED7';BLUE='#6992FF';TEAL='#3CDBBF';
STOP=set('the a an and or is are was were of to in for on with this that it as by from be have has had at we you they i he she not but if then than so can will would should'.split())
def words(s):return re.findall(r"[A-Za-z][A-Za-z'-]*",s.lower())
def summary(t,n=5):
 ss=[x.strip() for x in re.split(r'(?<=[.!?])\s+',t) if len(words(x))>3]; f=collections.Counter(w for w in words(t) if w not in STOP);rank=sorted(enumerate(ss),key=lambda x:sum(f[w] for w in words(x[1])),reverse=True)[:min(n,len(ss))];return [x[1] for x in sorted(rank)]
def keyterms(t,n=12):return collections.Counter(w for w in words(t) if w not in STOP and len(w)>3).most_common(n)
def easy(t):
 w=words(t);s=max(1,len(re.findall(r'[.!?]+',t)));sy=sum(max(1,len(re.findall(r'[aeiouy]+',x))) for x in w);return round(206.835-1.015*len(w)/s-84.6*sy/max(1,len(w)),1)
class App(tk.Tk):
 def __init__(self):super().__init__();self.title('AccessNotes — Accessible audio summarizer');self.geometry('1180x740');self.minsize(950,620);self.configure(bg=BG);self.large=False;self.build()
 def L(self,p,t,size=11,c=TEXT,b=False,**k):return tk.Label(p,text=t,bg=p['bg'],fg=c,font=('Segoe UI',size,'bold' if b else 'normal'),**k)
 def card(self,p):return tk.Frame(p,bg=CARD,highlightthickness=1,highlightbackground='#283A5E')
 def build(self):
  h=tk.Frame(self,bg=BG);h.pack(fill='x',padx=36,pady=(24,8));self.L(h,'ACCESSNOTES',12,TEAL,True).pack(anchor='w');self.L(h,'Accessibility-first audio summarizer',27,TEXT,True).pack(anchor='w');self.L(h,'Local transcript summarization • readable notes • no API • no server',11,MUTED).pack(anchor='w',pady=(3,0))
  controls=self.card(self);controls.pack(fill='x',padx=36,pady=12);self.status=self.L(controls,'Start with a transcript from your recording. Audio transcription is intentionally not included, so nothing is sent to a cloud service.',10,MUTED);self.status.pack(side='left',padx=16,pady=12);tk.Button(controls,text='Open .txt',command=self.open,bg=BLUE,fg='white',relief='flat',padx=13,pady=7,font=('Segoe UI',10,'bold')).pack(side='right',padx=8);tk.Button(controls,text='Large text',command=self.font,bg='#243A64',fg='white',relief='flat',padx=13,pady=7,font=('Segoe UI',10,'bold')).pack(side='right',padx=4)
  main=tk.Frame(self,bg=BG);main.pack(fill='both',expand=True,padx=36,pady=(0,24));main.columnconfigure(0,weight=1);main.columnconfigure(1,weight=1);main.rowconfigure(0,weight=1)
  a=self.card(main);a.grid(row=0,column=0,sticky='nsew',padx=(0,8));b=self.card(main);b.grid(row=0,column=1,sticky='nsew',padx=(8,0));self.L(a,'TRANSCRIPT',11,MUTED,True).pack(anchor='w',padx=18,pady=(16,7));self.src=tk.Text(a,bg='#0B172A',fg=TEXT,insertbackground=TEXT,relief='flat',wrap='word',font=('Segoe UI',11),padx=12,pady=12);self.src.pack(fill='both',expand=True,padx=18);self.src.insert('1.0','Speaker: Today we will learn about accessible media. A transcript helps people access spoken information. The main action is to provide clear notes and key terms after every lecture.')
  tk.Button(a,text='Create accessible notes',command=self.run,bg=TEAL,fg='#06151A',relief='flat',font=('Segoe UI',11,'bold'),pady=10).pack(fill='x',padx=18,pady=16)
  self.L(b,'ACCESSIBLE NOTES',11,MUTED,True).pack(anchor='w',padx=18,pady=(16,7));self.out=tk.Text(b,bg='#0B172A',fg=TEXT,relief='flat',wrap='word',font=('Segoe UI',11),padx=14,pady=12);self.out.pack(fill='both',expand=True,padx=18);self.out.config(state='disabled');tk.Button(b,text='Save notes .txt',command=self.save,bg=BLUE,fg='white',relief='flat',font=('Segoe UI',10,'bold'),pady=9).pack(fill='x',padx=18,pady=16)
 def open(self):
  p=filedialog.askopenfilename(filetypes=[('Text files','*.txt'),('All files','*.*')]);
  if p:
   try:self.src.delete('1.0','end');self.src.insert('1.0',Path(p).read_text(encoding='utf-8'));self.status.config(text='Transcript loaded locally: '+p.split('/')[-1])
   except Exception as e:messagebox.showerror('Cannot open',str(e))
 def run(self):
  t=self.src.get('1.0','end-1c').strip()
  if not t:return
  sm=summary(t);ks=keyterms(t);qs=[s for s in re.split(r'(?<=[.!?])\s+',t) if '?' in s];w=len(words(t));note='ACCESSIBLE STUDY NOTES\n\nQUICK SUMMARY\n'+'\n'.join('• '+x for x in sm)+'\n\nKEY TERMS\n'+'\n'.join(f'• {x} ({n} mentions)' for x,n in ks)+'\n\nQUESTIONS IN THE RECORDING\n'+('\n'.join('• '+x for x in qs) if qs else '• No question sentences detected.')+f'\n\nREADING GUIDE\n• Transcript words: {w}\n• Reading-ease estimate: {easy(t)}\n• Tip: Review the summary first, then use key terms to search the full transcript.'
  self.out.config(state='normal');self.out.delete('1.0','end');self.out.insert('1.0',note);self.out.config(state='disabled');self.status.config(text='Notes created locally. Review them against the original transcript for important detail.')
 def save(self):
  x=self.out.get('1.0','end-1c');
  if not x:return messagebox.showinfo('Nothing to save','Create notes first.')
  p=filedialog.asksaveasfilename(defaultextension='.txt',initialfile='accessible_notes.txt',filetypes=[('Text','*.txt')]);
  if p:Path(p).write_text(x,encoding='utf-8');messagebox.showinfo('Saved','Accessible notes saved locally.')
 def font(self):
  self.large=not self.large;size=15 if self.large else 11;self.src.config(font=('Segoe UI',size));self.out.config(font=('Segoe UI',size));self.status.config(text='Large-text mode enabled.' if self.large else 'Standard text size enabled.')
if __name__=='__main__':App().mainloop()
