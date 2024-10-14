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
bool formatMessage(byte code, string &smessage);
bool formatDataMessage(float xcoord, float ycoord, string &smessage);
bool sendMessage(string message);
string readMessage();

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

void formatMessage(byte code, string &smessage)
{
     string scode;
     scode = NumToStr(code);
     smessage = StrCat("2;", scode);
}

void formatDataMessage(float xcoord, float ycoord, string &smessage)
{
     string sxcoord, sycoord;
     sxcoord = NumToStr(ycoord);
     sycoord = NumToStr(ycoord);
     smessage = StrCat("3;", sxcoord, sycoord);
}

bool sendMessage(string message)
{
     return (SendMessage(9, message) ? true : false);
}

bool readMessage(string &receivedMsg)
{
       if (ReceiveMessage(0, true, message) == NO_ERR)
          return true;
       return false;
}

