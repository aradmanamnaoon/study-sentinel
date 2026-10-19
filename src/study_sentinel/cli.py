"""CLI for offline synthetic demo and audit."""
import argparse,json,sys
from pathlib import Path
from .contracts import Study,Scale
from .simulation import simulate
from .pipeline import run
from .reports import write_report
from .errors import StudyError

def main(argv:list[str]|None=None)->int:
    parser=argparse.ArgumentParser(prog="study-sentinel")
    sub=parser.add_subparsers(dest="command",required=True)
    demo=sub.add_parser("demo")
    demo.add_argument("--out",default="demo-study")
    demo.add_argument("--n",type=int,default=300)
    demo.add_argument("--seed",type=int,default=42)
    audit=sub.add_parser("analyze")
    audit.add_argument("--manifest",required=True)
    audit.add_argument("--csv",required=True)
    audit.add_argument("--out",default="study-report")
    audit.add_argument("--permutations",type=int,default=999)
    args=parser.parse_args(argv)
    try:
        if args.command=="demo":
            target=Path(args.out);target.mkdir(parents=True,exist_ok=True)
            simulate(n=args.n,seed=args.seed).to_csv(target/"synthetic_study.csv",index=False)
            config=Study("Synthetic stress/wellbeing study","participant_id","wellbeing","sleep_hours",
                ("age",),(Scale("stress",( "stress_1","stress_2","stress_3","stress_4","stress_5"),("stress_3",),1,5,3),),args.seed)
            (target/"study.json").write_text(json.dumps(config.as_dict(),indent=2)+"\n",encoding="utf8")
            print(f"generated synthetic study in {target}")
        else:
            files=write_report(run(Study.load(args.manifest),args.csv,permutations=args.permutations),args.out)
            print("\n".join(map(str,files)))
        return 0
    except (StudyError,ValueError,OSError) as exc:
        print(f"error: {exc}",file=sys.stderr)
        return 2
if __name__=="__main__": raise SystemExit(main())
