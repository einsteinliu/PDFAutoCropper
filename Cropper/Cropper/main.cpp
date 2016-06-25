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
#include "SteinCropper.h"
using namespace std;
using namespace cv;

int main()
{
	SteinCropper stCropper;
	stCropper.loadFiles(L".\\*.*");
	return 0;
	int k;
	Timer timer;
	Mat          origin,gray,rot,rowMat,rotWrap;
	origin = imread("Foucault-test.jpg");
	timer.Start();
	cvtColor(origin, gray, CV_BGR2GRAY);
	timer.Stop();
	cout << timer.Elapsed() << " ms color" << endl;
	resize(gray, gray, Size(0, 0), 0.5, 0.5);
	timer.Stop();
	cout << timer.Elapsed() << " ms resize" << endl;
	for (int i = 1; i < 5; i++)
	{
		rotWrap = cv::getRotationMatrix2D(Point2f(gray.cols / 2.0, gray.rows / 2.0), i, 1);
		warpAffine(gray, rot, rotWrap, gray.size());
		timer.Stop();
		cout<<timer.Elapsed() << " ms rot" << endl;
	}
	timer.Stop();
	cout << timer.Elapsed() << " ms done\n" << endl;
	imshow("rotated", rot);
	waitKey(0);

	cuda::GpuMat gOrigin, gGray, gRot, gRowMat;
	timer.Start();
	gOrigin.upload(origin);
	cuda::cvtColor(gOrigin, gGray, CV_BGR2GRAY);
	timer.Stop();
	cout << timer.Elapsed() << " ms color" << endl;
	cuda::resize(gGray, gGray, Size(0, 0), 0.5, 0.5);
	timer.Stop();
	cout << timer.Elapsed() << " ms resize" << endl;
	for (int i = 1; i < 5; i++)
	{
		cuda::rotate(gGray, gRot, gGray.size(), i); 
		gRot.download(rot);
		timer.Stop();
		cout <<"rot:"<< timer.Elapsed() << " ms rot" << endl;
	}
	timer.Stop();
	cout << timer.Elapsed() << " ms done" << endl;
	imshow("rotated", rot);
	waitKey(0);
	return 0;
}