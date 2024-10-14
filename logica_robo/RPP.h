# RPP protocol defines and functions

#ifndef __RPP__
#define __RPP__

// ------------ RPP defines ---------------------

// header
#define REQUEST  1
#define RESPONSE 2
#define POSITION 3

// request type messages
#define ACTIVATE 0
#define STATUS   1

// response type messages
#define SUCCESS   0
#define ERROR     1
#define COMPLETED 2
#define ONGOING   3

// the robot only response the request from
// supervisor
void parseMessage(string message, byte data[]);
string formatMessage(byte code);
string formatDataMessage(float xcoord, float ycoord);

#endif

void parserMessage(string message, byte data[])
{
     string type, value;
     byte type_b, value_b;
     type = message[0];
     value = message[2];
     type_b = StrToNum(type);
     value_b = StrToNum(value);
     if (type_b == 1) data[1] = 255;
     else data[0] = type_b;
     data[1] = value_b;
}

string formatMessage(byte code)
{
     string scode, formattedMessage;
     scode = NumToStr(code);
     formattedMessage = StrCat("2;", scode);
     return formattedMessage;
}

string formatDataMessage(float xcoord, float ycoord)
{
     string formattedMessage, sxcoord, sycoord;
     sxcoord = NumToStr(ycoord);
     sycoord = NumToStr(ycoord);
     formattedString = StrCat("3;", sxcoord, sycoord);
     return formattedMessage;
}
