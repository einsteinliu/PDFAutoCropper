#pragma once
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include "opencv2/imgproc.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/calib3d.hpp"
#include "opencv2/video.hpp"
#include "opencv2/cudalegacy.hpp"
#include "opencv2/cudaimgproc.hpp"
#include "opencv2/cudaarithm.hpp"
#include "opencv2/cudawarping.hpp"
#include "opencv2/cudafeatures2d.hpp"
#include "opencv2/cudafilters.hpp"
#include "opencv2/cudaoptflow.hpp"
#include "opencv2/cudabgsegm.hpp"
#include "HDTimer.h"
#include "opencv2/opencv_modules.hpp"
#include <vector>

using namespace std;
using namespace cv;

class SteinCropper
{
public:
	SteinCropper();
	~SteinCropper();
	void loadFiles(wstring folder);
	Mat cropTheImageGPU(string file);
	Mat cropTheImage(string file);
	void showDebugImage(cuda::GpuMat& gmat);
	void showDebugImage(Mat& mat);
	void saveProj(Mat &proj);
	bool checkIsTextBlock(Mat& patch);
private:
	vector<string> images;
	double maxAbsDiff(Mat &proj);
	vector<cv::Rect> detectAllTextCells(Mat &correctedImage);
	Point getTextPart(Mat &proj, vector<Rect> &textBlocks);
	double computeBestAngle(Mat &image, vector<double> angles);
};

