import ROOT

# from within CMSSW:
ROOT.gSystem.Load('libCondFormatsBTagObjects') 

# OR using standalone code:
ROOT.gROOT.ProcessLine('.L BTagCalibrationStandalone.cc+') 

calib = ROOT.BTagCalibration("csvv2", "CSVv2.csv")




fl = ["B", "C", "L"]
wp = ["L", "M", "T"]
workingpoint = [0., 0.605, 0.890, 0.980, 1.]


reader = {}
for i, w in enumerate(wp):
    reader[w] = {}
    reader[w][0] = ROOT.BTagCalibrationReader(calib, i, "mujets", "central")
    reader[w][1] = ROOT.BTagCalibrationReader(calib, i, "mujets", "up")
    reader[w][-1] = ROOT.BTagCalibrationReader(calib, i, "mujets", "down")


# in your event loop
print reader["L"][0].eval(0, 1.2, 400.)  # jet flavor, eta, pt



shape = {}

shFile = TFile("BTAG/BTagShapes.root", "READ")
shFile.cd()
if not shFile.IsZombie():
    for i, f in enumerate(wp):
        shape[f] = shFile.Get("j_bTagDiscr"+f)
else: print " - BTagWeight Error: No Shape File"

for i, f in enumerate(wp):
    shape[f].Smooth(100)
    shape[f].Rebin(10)
    shape[f].Scale(1./shape[f].Integral())


integral = {}
for i, f in enumerate(fl):
    integral[f] = []
    for j, w in enumerate(workingpoint):
        integral[f].append([ shape[f].Integral(shape[f].FindBin(w), shape[f].GetNbinsX()+1) ])


def returnNewWorkingPoint(f, p, pt, eta, sigma):
    if f<0 or f>2: print " - BTagWeight Error: unrecognized flavour"
    if p<0 or p>4: print " - BTagWeight Error: working point not defined"
    if p==0 or p==4: return workingpoint[p]

    Int = integral[fl[f]][p]
    if f==0: Int /= reader[wp[p]][sigma].eval(f, eta, pt)
    
    n = shape[f].GetNbinsX()+1
    step = 10
    #for (i=n; i>0; i=i-step):
    for i in list(reversed(range(0, n, step))):
        if shape[f].Integral(i-step, n) >= Int:
            #for (; i>0; i=step/10):
            for j in list(reversed(range(0, i, step/10))):
                if shape[f].Integral(j-step, n) >= Int:
                    return (j-0.5)/shape[f].GetNbinsX()
    
    return workingpoint[w]


def returnReshapedDiscr(f, discr, pt, eta, sigma=""):
    if discr<0.01 or discr>0.99: return discr
    if f<0 or f>2: return discr
    i0, i1 = 0, 4
    x0, x1 = 0., 1.
    
    for i in range(1, 5):
        if discr<=workingpoint[i]:
            x0 = workingpoint[i-1]
            x1 = workingpoint[i]
            i0 = i-1
            i1 = i
            break
    
    y0 = returnNewWorkingPoint(fl, i0, pt, eta, sigma)
    y1 = returnNewWorkingPoint(fl, i1, pt, eta, sigma)
    return y0 + (discr-x0)*((y1-y0)/(x1-x0))

#float BTagWeightInterface::ReturnNewWorkingPoint(int fl, int wp, float pt, float eta, int sigma) {
#  if(fl<0 || fl>2) {std::cout << " - BTagWeight Error: unrecognized flavour" << std::endl; return -1.;}
#  if(wp<0 || wp>4) {std::cout << " - BTagWeight Error: working point not defined" << std::endl; return -1.;}
#  if(wp==0 || wp==4) return WorkingPoint[wp];
#  
#  // Get original integral
#  //float Int=Shape[fl]->Integral(Shape[fl]->FindBin(WorkingPoint[wp]), Shape[fl]->GetNbinsX()+1);
#  float Int=Integral[fl][wp]; // Saves time
#  // Scale integral by Scale Factor with Error
#  if(fl==0) Int/=ReturnScaleFactor(wp, pt, eta, sigma);
#  else if(fl==1) Int/=ReturnScaleFactor(wp, pt, eta, 2*sigma);
#  else Int/=ReturnScaleFactorMistag(wp, pt, eta, sigma);
#  // Find new Discriminator value
#  // Fast scan, start from wp and go up
#  for(int i=Shape[fl]->GetNbinsX()+1; i>0; i=i-100) {
#    if(Shape[fl]->Integral(i-100, Shape[fl]->GetNbinsX()+1)>=Int) {
#      for(; i>0; i=i-10) {
#        if(Shape[fl]->Integral(i-10, Shape[fl]->GetNbinsX()+1)>=Int) {
#          for(; i>0; i=i-1) {
#            if(Shape[fl]->Integral(i, Shape[fl]->GetNbinsX()+1)>=Int) {
#              return ((float)i-0.5)/Shape[fl]->GetNbinsX();
#            }
#          }
#        }
#      }
#    }
#  }
#  // Integral Interpolation
#//  for(int i=Shape[fl]->GetNbinsX()+1; i>0; i--) {
#//    if(Shape[fl]->Integral(i, Shape[fl]->GetNbinsX()+1)>=Int) {
#//      float x0=Shape[fl]->Integral(i, Shape[fl]->GetNbinsX()+1);
#//      float x1=Shape[fl]->Integral(i+1, Shape[fl]->GetNbinsX()+1);
#//      float y0=Shape[fl]->GetXaxis()->GetBinLowEdge(i);
#//      float y1=Shape[fl]->GetXaxis()->GetBinLowEdge(i+1);
#//      return y0 + (Int-x0)*((y1-y0)/(x1-x0));
#//    }
#//  }
#  //std::cout << " - BTagWeight Warning: new working point " << wp << " not found" << std::endl;
#  return WorkingPoint[wp];
#}

#float BTagWeightInterface::ReturnReshapedDiscr(int fl, float discr, float pt, float eta, int sigma) {
#  if(discr<0.01) return discr;
#  if(discr>0.99) return discr;
#  if(fl<0 || fl>2) return discr;
#  int i0(0), i1(4);
#  float x0(0.), x1(1.);
#  // Find boundary old Discr values
#  for(int i=1; i<5; i++) {
#    if(discr<=WorkingPoint[i]) {
#      x0=WorkingPoint[i-1];
#      x1=WorkingPoint[i];
#      i0=i-1;
#      i1=i;
#      break;
#    }
#  }
#  // Find boundary new Discr values
#  float y0=ReturnNewWorkingPoint(fl, i0, pt, eta, sigma);
#  float y1=ReturnNewWorkingPoint(fl, i1, pt, eta, sigma);
#  // Interpolate
#  return y0 + (discr-x0)*((y1-y0)/(x1-x0));
#}
