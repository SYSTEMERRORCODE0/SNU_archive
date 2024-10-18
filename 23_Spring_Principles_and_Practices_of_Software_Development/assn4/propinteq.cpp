#include "llvm/IR/Dominators.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/PassManager.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"
#include <vector>

using namespace llvm;
using namespace std;

namespace {
class PropagateIntegerEquality
    : public PassInfoMixin<PropagateIntegerEquality> {
public:
  PreservedAnalyses run(Function &F, FunctionAnalysisManager &FAM) {
    struct P{
      StringRef bb1, bb2, name, op1, op2;
      Value *op1v;
    };

    int change = 1;

    /* until nothing to change */
    while(change == 1) {

    change = 0;

    typedef pair<BasicBlock*,StringRef> PBS;  // BB, ARG
    vector<PBS> args;
    //vector<Value> values;
    vector<BasicBlock*> bbs;
    vector<P> props;

    /* get BBs */
    for(auto &BB : F) {
      bbs.push_back(&BB);
    }

    /* get args of the function */
    for(auto &arg : F.args()) {
      if(bbs.size() > 0) {   //should be true
        args.push_back(PBS(bbs[0],arg.getName()));
      }
    }

    /* check ICmp eq, Br */
    DominatorTree &DT = FAM.getResult<DominatorTreeAnalysis>(F);
    for(auto &BB : F) {
      for(auto &I : BB) {

        /* put args into vector */
        if(I.hasName()) {
          args.push_back(PBS(&BB,I.getName()));
        }

        if(I.getOpcode() == Instruction::ICmp) {
          auto *icmp = dyn_cast<ICmpInst>(&I);
          if(icmp->getPredicate() != CmpInst::ICMP_EQ) continue;

          /* collect propinteq */
          BasicBlock *bb1,*bb2;
          StringRef arg1 = I.getOperand(0)->getName(), arg2 = I.getOperand(1)->getName();
          if(arg1 == arg2) continue;
          Value *val = I.getOperand(0);
          int whose_first = 0;
          for(PBS arg : args) {
            if(arg.second == arg1) bb1 = arg.first, whose_first = whose_first == 0 ? 1 : whose_first;
            if(arg.second == arg2) bb2 = arg.first, whose_first = whose_first == 0 ? 2 : whose_first;
          }

          if(bb1 == bb2) {
            if(whose_first == 2) swap(arg1, arg2), val = I.getOperand(1);
            props.push_back(P{BB.getName(), "", I.getName(), arg1, arg2, val});
          } else if(DT.dominates(bb1, bb2)) {
            props.push_back(P{BB.getName(), "", I.getName(), arg1, arg2, val});
          } else if(DT.dominates(bb2, bb1)){
            props.push_back(P{BB.getName(), "", I.getName(), arg2, arg1, val});
          } else {
            //pass. Not dominate
          }

        } else if(I.getOpcode() == Instruction::Br && I.getNumOperands() == 3) {

          /* "perhaps" check the BB and got it in */
          for(int i = 0; i < props.size(); i++) {
            if(I.getOperand(0)->getName() == props[i].name) {
            for(BasicBlock *j : bbs) {
              if(j->getName() == I.getOperand(2)->getName()) {
                props[i].bb2 = j->getName();
              }
            }
            }
          }
        }
      }
    }

    /* change the args */
    for(auto &BB : F) {
      for(auto &I : BB) {
        for(P prop : props) {
          if(prop.bb2 == "") continue;
          int op2i = -1;
          for(int i = 0; i < I.getNumOperands(); i++) {
            if(prop.op2 == I.getOperand(i)->getName()) op2i = i;
          }

          if(op2i == -1) continue;  // NO changable argument

          BasicBlock *bb1, *bb2;
          for(BasicBlock *bb : bbs) {
            if(bb->getName() == prop.bb1) bb1 = bb;
            if(bb->getName() == prop.bb2) bb2 = bb;
          }
          BasicBlockEdge BBE(bb1, bb2);
          if(DT.dominates(BBE, &BB)) {
            I.setOperand(op2i, prop.op1v);
            change = 1;
          }
        }
      }
    }

    }

    return PreservedAnalyses::all();
  }
};
} // namespace

extern "C" ::llvm::PassPluginLibraryInfo llvmGetPassPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "PropagateIntegerEquality", "v0.1",
          [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, FunctionPassManager &FPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "prop-int-eq") {
                    FPM.addPass(PropagateIntegerEquality());
                    return true;
                  }
                  return false;
                });
          }};
}
