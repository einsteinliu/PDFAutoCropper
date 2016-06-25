#include "SteinCropper.h"
#include <stdlib.h>


vector<string> GetFileNamesInDirectory(wstring directory) {
	vector<string> files;
	WIN32_FIND_DATA fileData;
	HANDLE hFind;
	if (!((hFind = FindFirstFile(directory.c_str(), &fileData)) == INVALID_HANDLE_VALUE)) {
		while (FindNextFile(hFind, &fileData)) {
			char str[256];
			wcstombs(str, fileData.cFileName, 256);
			string currFile = str;
			if (currFile.find("jpg")!=string::npos)
				files.push_back(str);
		}
	}
	FindClose(hFind);
	return files;
}

SteinCropper::SteinCropper()
{
	for (int i = -3; i <= 3; i++)
		roughAngles.push_back(i);
	
}


SteinCropper::~SteinCropper()
{
}

void SteinCropper::showDebugImage(Mat& mat)
{
	imshow("debug", mat);
	waitKey(0);
}

void SteinCropper::showDebugImage(cuda::GpuMat& gmat)
{
	Mat debugImg;
	gmat.download(debugImg);

}

double SteinCropper::maxAbsDiff(Mat &proj)
{
	double max = 0;
	double curr;
	for (int i = 1; i < proj.rows; i++)
	{
		curr = abs(proj.at<double>(i, 0) - proj.at<double>(i - 1, 0));
		if (max < curr)
			max = curr;
	}
	return max;
}

Mat SteinCropper::cropTheImage(string file)
{
	Mat original = imread(file);
	Mat gOrigin, gGray, gCurrRot, gProj, gProjR, gProjSub, gProjSubAbs;
	Mat rotWrap;
	double       maxDiff, minDiff, bestAngle;
	double       maxMaxDiff = 0;
	cv::Size     imSize = original.size();
	cvtColor(original, gGray, CV_BGR2GRAY);
	for (int i = 0; i < roughAngles.size(); i++)
	{
		double currAngle = roughAngles[i];

		rotWrap = cv::getRotationMatrix2D(Point2f(gGray.cols / 2.0, gGray.rows / 2.0), currAngle, 1);
		warpAffine(gGray, gCurrRot, rotWrap, gGray.size());
		//gProj = Mat(1, gCurrRot.cols, CV_64F);
		//showDebugImage(gCurrRot);
		reduce(gCurrRot, gProj, 1, CV_REDUCE_SUM, CV_64F);
		maxDiff = this->maxAbsDiff(gProj);
		//showDebugImage(gProj);
		//cv::rshift(gProj, 1, gProjR);
		//subtract(gProj, gProjR, gProjSub);
		//cv::abs(gProjSub, gProjSubAbs);
		//cv::minMax(gProjSubAbs, &minDiff, &maxDiff);
		if (maxDiff > maxMaxDiff)
		{
			maxMaxDiff = maxDiff;
			bestAngle = i;
		}
	}
	return original;
}

Mat SteinCropper::cropTheImageGPU(string file)
{
	Mat original = imread(file);
	Mat debugImg;
	cuda::GpuMat gOrigin, gGray, gCurrRot, gProj, gProjR, gProjSub, gProjSubAbs;
	double       maxDiff,minDiff,bestAngle;
	double       maxMaxDiff = 0;
	cv::Size     imSize = original.size();
	gOrigin.upload(original);
	cuda::cvtColor(gOrigin, gGray, CV_BGR2GRAY);
	for (int i = 0; i < roughAngles.size(); i++)
	{
		double currAngle = roughAngles[i];
		cuda::rotate(gGray, gCurrRot, imSize, currAngle);
		cuda::reduce(gCurrRot, gProj, 1, CV_REDUCE_SUM, CV_MAKE_TYPE(CV_MAT_DEPTH(32), gCurrRot.channels()));
		showDebugImage(gProj);
		cuda::rshift(gProj, 1, gProjR);
		cuda::subtract(gProj, gProjR, gProjSub);
		cuda::abs(gProjSub, gProjSubAbs);
		cuda::minMax(gProjSubAbs, &minDiff, &maxDiff);
		if (maxDiff > maxMaxDiff)
		{
			maxMaxDiff = maxDiff;
			bestAngle = i;
		}
	}
	return original;
}

void SteinCropper::loadFiles(wstring folder)
{
	images = GetFileNamesInDirectory(folder);
 	cropTheImage(images[0]);
}

