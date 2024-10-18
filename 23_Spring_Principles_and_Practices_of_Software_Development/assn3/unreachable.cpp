#include "llvm/IR/PassManager.h"
#include "llvm/Passes/PassBuilder.h"
#include "llvm/Passes/PassPlugin.h"
#include "llvm/Support/raw_ostream.h"
#include <string>
#include <vector>
#include <map>
#include <queue>
#define MAXBB 100000
using namespace llvm;
using namespace std;
typedef pair<StringRef,int> PSI;

namespace {
class MyUnreachablePass : public PassInfoMixin<MyUnreachablePass> {
public:
  PreservedAnalyses run(Function &F, FunctionAnalysisManager &FAM) {
    map<StringRef, int> name_to_num;
    vector<int> vec_path[MAXBB];
    bool reachable[MAXBB]={1};

    /* save all BB name */
    for(auto &BB : F) {
      name_to_num.insert(PSI(BB.getName(), name_to_num.size()));
    }

    /* collect edges */
    for(auto &BB : F) {
      for(auto &I : BB) {
        switch(I.getOpcode()) {
        case Instruction::Br: {
          if(I.getNumOperands() == 3) { // br %cond, label %a, label %b
            vec_path[name_to_num[BB.getName()]].push_back(name_to_num[I.getOperand(1)->getName()]);
            vec_path[name_to_num[BB.getName()]].push_back(name_to_num[I.getOperand(2)->getName()]);
          } else {  // br label %a
            vec_path[name_to_num[BB.getName()]].push_back(name_to_num[I.getOperand(0)->getName()]);
          }
          break;
        }
        case Instruction::Switch: { // I implemented for switch inst, for another(PERHAPS?) testcases
          for(int i = 1; i < I.getNumOperands(); i += 2) {
            vec_path[name_to_num[BB.getName()]].push_back(name_to_num[I.getOperand(i)->getName()]);
          }
        }
        default:
          // Unknown instruction including ret
          break;
        }
      }
    }

    /* check reachable by BFS */
    queue<int> q;
    q.push(0);
    while(!q.empty()) {
      int i = q.front();
      q.pop();
      for(int j : vec_path[i]) {
        if(reachable[j] == 0) {
          reachable[j] = 1;
          q.push(j);
        }
      }
    }

    /* output unreachable BBs, automatically sorted by map */
    for(PSI i : name_to_num) {
      if(reachable[i.second] == 0) {
        outs() << i.first << "\n";
      }
    }
    
    return PreservedAnalyses::all();
  }
};
} // namespace

extern "C" ::llvm::PassPluginLibraryInfo llvmGetPassPluginInfo() {
  return {LLVM_PLUGIN_API_VERSION, "MyUnreachablePass", "v0.1",
          [](PassBuilder &PB) {
            PB.registerPipelineParsingCallback(
                [](StringRef Name, FunctionPassManager &FPM,
                   ArrayRef<PassBuilder::PipelineElement>) {
                  if (Name == "my-unreachable") {
                    FPM.addPass(MyUnreachablePass());
                    return true;
                  }
                  return false;
                });
          }};
}
