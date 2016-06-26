#include "SteinCropper.h"
#include <stdlib.h>
#include <fstream>

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
}


SteinCropper::~SteinCropper()
{
}

void SteinCropper::saveProj(Mat &proj)
{
	std::ofstream fs("log.txt");
	Mat toSave = proj.clone();
	if (proj.rows == 1)
		transpose(toSave, toSave);
	for (int i = 0; i < toSave.rows; i++)
		fs << toSave.at<double>(i, 0) << endl;
	fs.close();
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
	Mat rotWrap,bestRot,bestProj;
	double       maxDiff, minDiff;
	double       maxMaxDiff = 0;
	double       lastMaxDiff = 0;
	cv::Size     imSize = original.size();
	//convert to gray image
	cvtColor(original, gGray, CV_BGR2GRAY);
	double ratio = 1500.0 / gGray.rows;
	if (ratio<1)
	{
		resize(gGray, gGray, cv::Size(), ratio, ratio);
	}
	//find the best correction angle
	vector<double> angles;
	double steps[3] = { 1.0, 0.2, 0.05 };
	double bestAngle = 0;
	for (int n = 0; n < 2; n++)
	{
		double step = steps[n];
		for (int i = 5; i >= -5; i--)
		{
			angles.push_back(bestAngle + i*step);
		}
		bestAngle = computeBestAngle(gGray, angles);
		angles.clear();
	}
	rotWrap = cv::getRotationMatrix2D(Point2f(gGray.cols / 2.0, gGray.rows / 2.0), bestAngle, 1);
	warpAffine(gGray, gGray, rotWrap, gGray.size());
	
	vector<Rect> textCells = detectAllTextCells(gGray);
	gGray = 255 - gGray;
	//showDebugImage(gGray);
	reduce(gGray, bestProj, 1, CV_REDUCE_SUM, CV_64F);
	//saveProj(bestProj);
	//get upper lower bound, rows
	Point ulBound = getTextPart(bestProj, textCells);
	reduce(gGray, bestProj, 0, CV_REDUCE_SUM, CV_64F);
	//get left right bound, cols
	Point lrBound = getTextPart(bestProj, textCells);
	ulBound.x = cvRound(ulBound.x / ratio);
	ulBound.y = cvRound(ulBound.y / ratio);
	lrBound.x = cvRound(lrBound.x / ratio);
	lrBound.y = cvRound(lrBound.y / ratio);
	return original(Rect(lrBound.x, ulBound.x, lrBound.y - lrBound.x, ulBound.y - ulBound.x));
}

double SteinCropper::computeBestAngle(Mat &image, vector<double> angles)
{
	Mat rotWrap, currRot, currProj;
	double maxDiff;
	double maxMaxDiff = 0;
	double lastMaxDiff = 0;
	double bestAngle;
	for (int i = 0; i < angles.size(); i++)
	{
		double currAngle = angles[i];
		rotWrap = cv::getRotationMatrix2D(Point2f(image.cols / 2.0, image.rows / 2.0), currAngle, 1);
		warpAffine(image, currRot, rotWrap, image.size());
		reduce(currRot, currProj, 1, CV_REDUCE_SUM, CV_64F);
		maxDiff = maxAbsDiff(currProj);
		//if (maxDiff < lastMaxDiff)
		if (maxDiff > maxMaxDiff)
		{
			//rotWrap = cv::getRotationMatrix2D(Point2f(image.cols / 2.0, image.rows / 2.0), roughAngles[i - 1], 1);
			//warpAffine(image, image, rotWrap, image.size());
			//return angles[i - 1];
			maxMaxDiff = maxDiff;
			bestAngle = angles[i];
		}
		else
			lastMaxDiff = maxDiff;
	}
	return bestAngle;
}

Point SteinCropper::getTextPart(Mat &proj, vector<Rect> &textBlocks)
{
	int leftBound = 9999;
	int rightBound = 0;
	int threshold = 5*255;
	double value;
	bool vert = (proj.cols == 1);
	if (!vert)
		transpose(proj, proj);
	for (int i = 0; i < 5; i++)
	{
		proj.at<double>(i, 0) = 0;
		proj.at<double>(proj.rows-i-1,0) = 0;
	}
	for (int i = 0; i < textBlocks.size(); i++)
	{
		Rect cell = textBlocks[i];
		int currLeft;
		int currRight;
		if (vert)
		{
			currLeft = cell.y;
			currRight = cell.y + cell.height;
		}
		else
		{
			currLeft = cell.x;
			currRight = cell.x + cell.width;
		}
		int curr;
		for (int l = 0; l < currLeft; l++)
		{
			curr = currLeft - l;
			value = proj.at<double>(curr, 0);
			if ((value > threshold) && (curr < leftBound))
			{
				leftBound = curr;
				if (leftBound < 10)
					leftBound = curr;
			}

		}
		for (int l = currRight - 1; l < proj.rows; l++)
		{
			curr = l;
			if ((proj.at<double>(curr, 0) > threshold) && (curr > rightBound))
				rightBound = curr;
		}
	}
	if (leftBound == 9999)
		leftBound = 0;
	if (rightBound == 0)
		rightBound = proj.rows - 1;
	if (leftBound > 10)
		leftBound = leftBound - 10;
	if (rightBound < (proj.rows - 10))
		rightBound = rightBound + 10;

	return Point(leftBound, rightBound);
}

bool SteinCropper::checkIsTextBlock(Mat& patch)
{
	Point2f realCenter(patch.cols*0.5, patch.rows*0.5);
	double  threshold = patch.cols*0.1;
	Point2f blackCenter(0, 0);
	Point2f whiteCenter(0, 0);
	int		blackPixels = 0;
	int     whitePixels = 0;
	for (int x = 0; x < patch.cols; x++)
	{
		for (int y = 0; y < patch.rows; y++)
		{
			if (255 == patch.at<uchar>(y, x))
			{
				whiteCenter.x += x;
				whiteCenter.y += y;
				whitePixels++;
			}
			else
			{
				blackCenter.x += x;
				blackCenter.y += y;
				blackPixels++;
			}
		}
	}
	if (0 == blackPixels)
		blackCenter = Point2f(-1, -1);
	else
		blackCenter = blackCenter / blackPixels;

	if (0 == whitePixels)
		whiteCenter = Point2f(-1, -1);
	else
		whiteCenter = whiteCenter / whitePixels;

	Point2f deltaW = (whiteCenter - realCenter);
	Point2f deltaB = (blackCenter - realCenter);
	deltaW.x = abs(deltaW.x);
	deltaW.y = abs(deltaW.y);
	deltaB.x = abs(deltaW.x);
	deltaB.y = abs(deltaB.y);
	if ((deltaW.x < threshold) && (deltaW.y < threshold) && (deltaB.x < threshold) && (deltaB.y < threshold))
	{
		//showDebugImage(patch);
		return true;
	}
	else
        return false;
}

vector<cv::Rect> SteinCropper::detectAllTextCells(Mat &image)
{
	int cellSize = (int)image.cols*0.1;
	if (cellSize < 15)
		cellSize = 15;
	int currCellX = 0;
	int currCellY = 0;
	int currCellWidth = 0;
	int currCellHeight = 0;
	int nextX = 0;
	int nextY = 0;
	vector<Rect> textCells;
	while (currCellX < image.cols)
	{
		currCellWidth = cellSize;
		int currCellXEnd = currCellX + currCellWidth;
		nextX = currCellXEnd;
		if (currCellXEnd > image.cols)
		{
			currCellXEnd = image.cols - 1;
			currCellWidth = image.cols - currCellX - 1;
		}
		while (currCellY < image.rows)
		{
			currCellHeight = cellSize;
			int currCellYEnd = currCellY + currCellHeight;
			nextY = currCellYEnd;
			if (currCellYEnd > image.rows)
			{
				currCellYEnd = image.rows - 1;
				currCellHeight = image.rows - currCellY - 1;
				nextY = 0;
			}
			if (checkIsTextBlock(image(Rect(currCellX, currCellY, currCellWidth, currCellHeight))))
				textCells.push_back(Rect(currCellX, currCellY, currCellWidth, currCellHeight));
			currCellY = nextY;
			if (nextY == 0)
				break;
		}
		currCellX = nextX;
	}
	return textCells;
}


Mat SteinCropper::cropTheImageGPU(string file)
{
	Mat original = imread(file);
	/*Mat debugImg;
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
	}*/
	return original;
}

void SteinCropper::loadFiles(wstring folder)
{
	images = GetFileNamesInDirectory(folder+L"\\*.*");
	char str[256];
	wcstombs(str, folder.c_str(), 256);
	string stdFolder = str;
	string saveFolder = stdFolder + "_cropped";
	CreateDirectoryA(saveFolder.c_str(), NULL);
	Timer timer;
	for (int i = 0; i < images.size(); i++)
	{
		timer.Start();
		Mat croppedImage = cropTheImage(stdFolder + "\\" + images[i]);
		imwrite(saveFolder + "\\" + images[i], croppedImage);
		timer.Stop();
		cout << timer.Elapsed() << " ms\n";
	}
}

