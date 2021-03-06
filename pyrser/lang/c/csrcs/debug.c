/*
** Copyright (C) 2012 Candiotti Adrien 
**
** This program is free software: you can redistribute it and/or modify
** it under the terms of the GNU General Public License as published by
** the Free Software Foundation, either version 3 of the License, or
** (at your option) any later version.
**
** This program is distributed in the hope that it will be useful,
** but WITHOUT ANY WARRANTY; without even the implied warranty of
** MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
**
** See the GNU General Public License for more details.
**
** You should have received a copy of the GNU General Public License
** along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
#include <stdlib.h>
#include <stdio.h>
#include "Base.h"
#include "Callback.h"
#include "ParsingBase.h"
#include "Primitives.h"
#include "Lifo.h"
#include "Capture.h"

/*
** These class were generated by the Pyworker tool.
**
** If any problem was encountered, for exemple if you're
** sure that generated code is wrong, contact me at:
** 
** adrien.candiotti@gmail.com
**
*/


bool		__debug__debugRule(s_ctx* oParentCtx);

/*
** debug::debug ::= [ "toto" #num ] | [ #identifier #string ]
** ;
*/
bool		__debug__debugRule(s_ctx* oParentCtx)
{
  s_ctx		oLocalCtx = {{NULL, 0}, &(oParentCtx)->localCapture};
  
  (void)oLocalCtx;
  if (true
/*
	    && alt(\
                 Expression(\
                         ReadText("toto")\
                         ,ReadInteger)\
                 ,Expression(\
                         ReadIdentifier\
                         ,ReadCString))\
*/
      && until(ReadText("lol"))
)
    return (true);
  return (false);
}
